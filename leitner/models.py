from django.db import models
from sorl.thumbnail.fields import ImageWithThumbnailsField
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from random import randint
from hashcolor import color, make_contrasting
from south.modelsinspector import add_introspection_rules

add_introspection_rules(
    [],
    ["sorl.thumbnail.fields.ImageWithThumbnailsField",
     ])


# Leitner's intervals
INTERVALS = [
    (5, "seconds"), (25, "seconds"), (2 * 60, "seconds"),
    (10 * 60, "seconds"), (1, "hours"), (5, "hours"),
    (1, "days"), (5, "days"), (25, "days"),
    (4 * 4, "weeks"), (2 * 52, "weeks")]


class Face(models.Model):
    content = models.TextField(default="", blank=True)
    image = ImageWithThumbnailsField(
        upload_to="faces",
        thumbnail={
            'size': (200, 200)
        }, blank=True)
    tex = models.TextField(default="", blank=True)

    def size(self):
        s = 800 / len(self.content)
        if s < 16:
            s = 16
        if s > 200:
            s = 200
        return s


class Deck(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey(User)

    def cards(self):
        return self.card_set.all()

    def num_cards(self):
        return self.card_set.all().count()

    def num_cards_due(self, user):
        return UserCard.objects.filter(
            user=user,
            rung__gte=0,
            card__deck=self,
            due__lte=datetime.now()).count()

    def usercards(self, user):
        return UserCard.objects.filter(
            user=user,
            card__deck=self
        )

    def bgcolor(self):
        return color(self.name)

    def fgcolor(self):
        return "%02x%02x%02x" % make_contrasting(self.bgcolor())

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/decks/%d/" % self.id


class Card(models.Model):
    front = models.ForeignKey(Face, related_name="front")
    back = models.ForeignKey(Face, related_name="back")
    added = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)
    deck = models.ForeignKey(Deck)

    def get_absolute_url(self):
        return "/cards/%d/" % self.id

    def usercard(self, user):
        return UserCard.objects.get(card=self, user=user)


def user_decks(user):
    return Deck.objects.filter(user=user)


def first_due_card(user):
    r = UserCard.objects.filter(user=user,
                                due__lte=datetime.now(),
                                rung__gte=0).order_by('due')
    if r.count() > 0:
        return r[0]
    else:
        return None


def closest_due_card(user):
    r = UserCard.objects.filter(user=user,
                                due__lte=datetime.now(),
                                rung__gte=0).order_by('due')
    if r.count() > 0:
        now = datetime.now()
        alldue = list(r)
        alldue.sort(key=lambda x: abs(x.due - now))
        return alldue[0]
    else:
        return None


def first_due_deck_card(user, deck):
    r = UserCard.objects.filter(user=user,
                                card__deck=deck,
                                due__lte=datetime.now(),
                                rung__gte=0).order_by('due')
    if r.count() > 0:
        return r[0]
    else:
        return None


def random_untested_card(user):
    r = UserCard.objects.filter(user=user, rung=-1)
    c = r.count()
    if c > 0:
        # do a stupid loop to work down by priority
        # TODO: replace with better query that finds the highest priority
        # available and just does that
        for p in range(10, 0, -1):
            res = random_untested_from_priority(user, p)
            if res is not None:
                return res
    else:
        # no untested cards
        return None


def random_untested_deck_card(user, deck):
    r = UserCard.objects.filter(user=user, rung=-1, card__deck=deck)
    c = r.count()
    if c > 0:
        # do a stupid loop to work down by priority
        # TODO: replace with better query that finds the highest priority
        # available and just does that
        for p in range(10, 0, -1):
            res = random_untested_from_priority(user, p)
            if res is not None:
                return res
    else:
        # no untested cards
        return None


def random_untested_from_priority(user, priority):
    r = UserCard.objects.filter(user=user, rung=-1, priority=priority)
    c = r.count()
    if c > 0:
        return r[randint(0, c - 1)]
    else:
        # no untested cards
        return None


def next_card(user):
    card = closest_due_card(user)
    if card is None:
        card = random_untested_card(user)
    return card


def next_deck_card(user, deck):
    card = first_due_deck_card(user, deck)
    if card is None:
        card = random_untested_deck_card(user, deck)
    return card


def first_due(user):
    r = UserCard.objects.filter(user=user, rung__gte=0).order_by("due")
    if r.count() > 0:
        return r[0]


def first_deck_due(user, deck):
    r = UserCard.objects.filter(user=user,
                                rung__gte=0,
                                card__deck=deck).order_by("due")
    if r.count() > 0:
        return r[0]


def recent_tests(user, n=100):
    return UserCardTest.objects.filter(
        usercard__user=user
    ).order_by("-timestamp")[:n]


class UserCard(models.Model):
    user = models.ForeignKey(User)
    card = models.ForeignKey(Card)
    priority = models.PositiveSmallIntegerField(default=1)
    due = models.DateTimeField(blank=True)
    # -1 means never presented to the user
    rung = models.SmallIntegerField(default=-1)
    # number right out of the last 10 tests
    ease = models.PositiveSmallIntegerField(default=5)

    def update_due(self):
        """ figure out the next due date for this card based on rung,
        difficulty, and current datetime """

        # if rung == -1, the user has never been presented with this card,
        # so we should never be here
        if self.rung == -1:
            return
        if self.rung > len(INTERVALS) - 1:
            self.rung = len(INTERVALS) - 1

        (n, u) = INTERVALS[self.rung]

        # extend interval based on ease. Ie, if they've gotten it right
        # 10 times out of 10, the interval gets doubled. 0 out of the last 10,
        # we stick with leitner's interval. Anything in between is proportional

        n *= (1.0 + (self.ease / 10.0))
        d = timedelta(**{u: n})
        now = datetime.now()
        self.due = now + d
        self.save()

    def update_rung(self, interval):
        intervals = INTERVALS[:]
        intervals.reverse()
        rung = 10
        for (n, u) in intervals:
            li = timedelta(**{u: n})
            if interval > li:
                # upgrade to either rung + 1 or the rung
                # that matches the interval
                self.rung = max(rung, self.rung + 1)
                break
            rung -= 1
        else:
            # tested within 5 seconds of the card being added
            if self.rung < 1:
                self.rung = 1

    def test_correct(self):
        """ user got it right, so we update accordingly """
        old_rung = self.rung
        q = self.usercardtest_set.all().order_by("-timestamp")
        if self.ease < 10:
            self.ease += 1

        if q.count() == 0:
            # never tested before
            # find the interval between now and when the card was added
            # which self.due should be set to currently
            # and calculate rung based on that
            now = datetime.now()
            interval = now - self.due
            self.update_rung(interval)
        else:
            # if the time since the last passed test was greater than one of
            # the intervals, make sure that it gets bumped up to at least
            # that rung
            last_correct = q[0].timestamp
            now = datetime.now()
            interval = now - last_correct
            self.update_rung(interval)
        UserCardTest.objects.create(usercard=self, correct=True,
                                    old_rung=old_rung, new_rung=self.rung)
        self.update_due()

    def test_wrong(self):
        UserCardTest.objects.create(usercard=self, correct=False,
                                    old_rung=self.rung, new_rung=0)
        self.rung = 0
        self.ease -= 1
        if self.ease < 0:
            self.ease = 0
        self.update_due()


def percent_right(user):
    """ returns percentage right for user """
    total = UserCardTest.objects.filter(
        usercard__user=user).count()
    right = UserCardTest.objects.filter(
        usercard__user=user, correct=True).count()
    return float(right) / float(total) * 100.0


def priority_stats(user):
    """ stats for cards of each priority """
    for p in range(10, 0, -1):
        yield dict(priority=p,
                   tested=UserCard.objects.filter(user=user, priority=p,
                                                  rung__gte=0).count(),
                   untested=UserCard.objects.filter(user=user, priority=p,
                                                    rung=-1).count(),
                   )


def rungs_stats(user):
    # TODO: convert to more efficient sql query
    d = dict()
    for x in range(-1, 11):
        d[x] = 0

    for uc in UserCard.objects.filter(user=user, rung__gte=0):
        d[uc.rung] = d[uc.rung] + 1

    for i in range(11):
        yield dict(rung=i, cards=d[i])


def ease_stats(user):
    # TODO: convert to more efficient sql query
    d = dict()
    for x in range(-1, 11):
        d[x] = 0

    for uc in UserCard.objects.filter(user=user, rung__gte=0):
        d[uc.ease] = d[uc.ease] + 1

    for i in range(11):
        yield dict(ease=i, cards=d[i])


def total_tested(user):
    return UserCard.objects.filter(user=user, rung__gte=0).count()


def total_untested(user):
    return UserCard.objects.filter(user=user, rung=-1).count()


def total_due(user):
    return UserCard.objects.filter(user=user, rung__gte=0,
                                   due__lte=datetime.now()).count()


def total_deck_due(user, deck):
    return UserCard.objects.filter(user=user, rung__gte=0,
                                   card__deck=deck,
                                   due__lte=datetime.now()).count()


def next_hour_due(user):
    return UserCard.objects.filter(
        user=user, rung__gte=0,
        due__lte=datetime.now() + timedelta(hours=1),
        due__gte=datetime.now()).count()


def next_day_due(user):
    return UserCard.objects.filter(
        user=user, rung__gte=0,
        due__lte=datetime.now() + timedelta(days=1),
        due__gte=datetime.now() + timedelta(hours=6)).count()


def next_six_hours_due(user):
    return UserCard.objects.filter(
        user=user, rung__gte=0,
        due__lte=datetime.now() + timedelta(hours=6),
        due__gte=datetime.now() + timedelta(hours=1)).count()


def next_week_due(user):
    return UserCard.objects.filter(
        user=user, rung__gte=0, due__lte=datetime.now() + timedelta(weeks=1),
        due__gte=datetime.now() + timedelta(days=1)).count()


def next_month_due(user):
    return UserCard.objects.filter(
        user=user, rung__gte=0, due__lte=datetime.now() + timedelta(weeks=4),
        due__gte=datetime.now() + timedelta(weeks=1)).count()


def overdue_dates(user):
    now = datetime.now()
    return [(now - u.due).seconds
            for u
            in UserCard.objects.filter(user=user, rung__gte=0).order_by("due")
            if u.due < now]


def due_dates(user):
    now = datetime.now()
    return [(u.due - now).seconds
            for u
            in UserCard.objects.filter(user=user, rung__gte=0).order_by("due")
            if u.due > now]


def clumped_due_dates(user, num_clumps=50):
    data = due_dates(user)
    return clump(data, num_clumps)


def clumped_overdue_dates(user, num_clumps=10):
    data = overdue_dates(user)
    return clump(data, num_clumps)


def clump(data, num_clumps):
    if len(data) <= num_clumps:
        return []
    maxn = max(data)
    minn = min(data)

    r = maxn - minn
    clumpsize = r / num_clumps

    clumps = [len([x for x in data if x >= clump and x < clump + clumpsize])
              for clump in range(minn, maxn, clumpsize)]
    maxclump = max(clumps)
    return ["%02x" % x for x in
            [int(255 - (255 * float(x) / float(maxclump))) for x in clumps]]


class UserCardTest(models.Model):
    """ represents an instance of a user being tested on a given card.
    basically here for logging/statistics/history purposes. might be possible
    to remove """
    usercard = models.ForeignKey(UserCard)
    timestamp = models.DateTimeField(auto_now=True)
    correct = models.BooleanField(default=True)
    old_rung = models.SmallIntegerField(default=0)
    new_rung = models.SmallIntegerField(default=0)

    def rung_diff(self):
        return self.new_rung - self.old_rung
