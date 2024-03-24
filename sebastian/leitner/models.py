from datetime import datetime, timedelta
from random import randint
from typing import Optional

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet

from sebastian.hashcolor import color, make_contrasting


class Face(models.Model):
    content = models.TextField(default="", blank=True)

    def size(self) -> float:
        s = 800 / len(self.content)
        if s < 16:
            s = 16
        if s > 200:
            s = 200
        return s


class Deck(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def cards(self) -> QuerySet["Card"]:
        return self.card_set.all()

    def num_cards(self) -> int:
        return self.card_set.all().count()

    def num_cards_due(self, user: User) -> int:
        return UserCard.objects.filter(
            user=user, rung__gte=0, card__deck=self, due__lte=datetime.now()
        ).count()

    def num_unlearned(self, user: User) -> int:
        return UserCard.objects.filter(
            user=user, rung=-1, card__deck=self
        ).count()

    def usercards(self, user: User) -> QuerySet["UserCard"]:
        return UserCard.objects.filter(user=user, card__deck=self)

    def bgcolor(self) -> str:
        return color(self.name)

    def fgcolor(self) -> str:
        return "%02x%02x%02x" % make_contrasting(self.bgcolor())

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return "/decks/%d/" % self.id


class Card(models.Model):
    front = models.ForeignKey(
        Face, related_name="front", on_delete=models.CASCADE
    )
    back = models.ForeignKey(
        Face, related_name="back", on_delete=models.CASCADE
    )
    added = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)

    def get_absolute_url(self) -> str:
        return "/cards/%d/" % self.id

    def usercard(self, user: User) -> "UserCard":
        return UserCard.objects.get(card=self, user=user)


def user_decks(user: User) -> QuerySet[Deck]:
    return Deck.objects.filter(user=user)


def first_due_card(user: User) -> Optional["UserCard"]:
    return (
        UserCard.objects.filter(
            user=user, due__lte=datetime.now(), rung__gte=0
        )
        .order_by("due")
        .first()
    )


def closest_due_card(user: User) -> Optional["UserCard"]:
    r = UserCard.objects.filter(
        user=user, due__lte=datetime.now(), rung__gte=0
    ).order_by("due")
    if r.count() > 0:
        now = datetime.now()
        alldue = list(r)
        alldue.sort(key=lambda x: abs(x.due - now))
        return alldue[0]
    else:
        return None


def first_due_deck_card(user: User, deck: Deck) -> Optional["UserCard"]:
    return (
        UserCard.objects.filter(
            user=user, card__deck=deck, due__lte=datetime.now(), rung__gte=0
        )
        .order_by("due")
        .first()
    )


def random_untested_card(user: User) -> Optional["UserCard"]:
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
    # no untested cards
    return None


def random_untested_deck_card(user: User, deck: Deck) -> Optional["UserCard"]:
    r = UserCard.objects.filter(user=user, rung=-1, card__deck=deck)
    c = r.count()
    if c > 0:
        # do a stupid loop to work down by priority
        # TODO: replace with better query that finds the highest priority
        # available and just does that
        for p in range(10, 0, -1):
            res = random_untested_from_priority_in_deck(user, p, deck)
            if res is not None:
                return res
    # no untested cards
    return None


def random_untested_from_priority(
    user: User, priority: int
) -> Optional["UserCard"]:
    r = UserCard.objects.filter(user=user, rung=-1, priority=priority)
    c = r.count()
    if c > 0:
        return r[randint(0, c - 1)]  # nosec
    # no untested cards
    return None


def random_untested_from_priority_in_deck(
    user: User, priority: int, deck: Deck
) -> Optional["UserCard"]:
    r = UserCard.objects.filter(
        user=user, rung=-1, priority=priority, card__deck=deck
    )
    c = r.count()
    if c > 0:
        return r[randint(0, c - 1)]  # nosec
    # no untested cards
    return None


def next_card(user: User) -> Optional["UserCard"]:
    card = closest_due_card(user)
    if card is None:
        card = random_untested_card(user)
    return card


def next_deck_card(user: User, deck: Deck) -> Optional["UserCard"]:
    card = first_due_deck_card(user, deck)
    if card is None:
        card = random_untested_deck_card(user, deck)
    return card


def first_due(user: User) -> Optional["UserCard"]:
    r = UserCard.objects.filter(user=user, rung__gte=0).order_by("due")
    if r.count() > 0:
        return r[0]
    return None


def first_deck_due(user: User, deck: Deck) -> Optional["UserCard"]:
    return (
        UserCard.objects.filter(user=user, rung__gte=0, card__deck=deck)
        .order_by("due")
        .first()
    )


def recent_tests(user: User, n: int = 100) -> QuerySet["UserCardTest"]:
    return UserCardTest.objects.filter(usercard__user=user).order_by(
        "-timestamp"
    )[:n]


class UserCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    priority = models.PositiveSmallIntegerField(default=1)
    due = models.DateTimeField(blank=True)
    # -1 means never presented to the user
    rung = models.SmallIntegerField(default=-1)
    # number right out of the last 10 tests
    ease = models.PositiveSmallIntegerField(default=5)

    def get_absolute_url(self) -> str:
        return "/cards/%d/" % self.id


def percent_right(user: User) -> float:
    """returns percentage right for user"""
    total = UserCardTest.objects.filter(usercard__user=user).count()
    right = UserCardTest.objects.filter(
        usercard__user=user, correct=True
    ).count()
    return float(right) / float(total) * 100.0


def priority_stats(user: User):
    """stats for cards of each priority"""
    for p in range(10, 0, -1):
        yield pstat(user, p)


def pstat(user: User, p: int):
    return dict(
        priority=p,
        tested=UserCard.objects.filter(
            user=user, priority=p, rung__gte=0
        ).count(),
        untested=UserCard.objects.filter(
            user=user, priority=p, rung=-1
        ).count(),
    )


def next_hour_due(user: User) -> int:
    return UserCard.objects.filter(
        user=user,
        rung__gte=0,
        due__lte=datetime.now() + timedelta(hours=1),
        due__gte=datetime.now(),
    ).count()


def next_day_due(user: User) -> int:
    return UserCard.objects.filter(
        user=user,
        rung__gte=0,
        due__lte=datetime.now() + timedelta(days=1),
        due__gte=datetime.now() + timedelta(hours=6),
    ).count()


def next_six_hours_due(user: User) -> int:
    return UserCard.objects.filter(
        user=user,
        rung__gte=0,
        due__lte=datetime.now() + timedelta(hours=6),
        due__gte=datetime.now() + timedelta(hours=1),
    ).count()


def next_week_due(user: User) -> int:
    return UserCard.objects.filter(
        user=user,
        rung__gte=0,
        due__lte=datetime.now() + timedelta(weeks=1),
        due__gte=datetime.now() + timedelta(days=1),
    ).count()


def next_month_due(user: User) -> int:
    return UserCard.objects.filter(
        user=user,
        rung__gte=0,
        due__lte=datetime.now() + timedelta(weeks=4),
        due__gte=datetime.now() + timedelta(weeks=1),
    ).count()


def overdue_dates(user: User) -> list[int]:
    now = datetime.now()
    return [
        (now - u.due).seconds
        for u in UserCard.objects.filter(user=user, rung__gte=0).order_by(
            "due"
        )
        if u.due < now
    ]


def due_dates(user: User) -> list[int]:
    now = datetime.now()
    return [
        (u.due - now).seconds
        for u in UserCard.objects.filter(user=user, rung__gte=0).order_by(
            "due"
        )
        if u.due > now
    ]


class UserCardTest(models.Model):
    """represents an instance of a user being tested on a given card.
    basically here for logging/statistics/history purposes. might be possible
    to remove"""

    usercard = models.ForeignKey(UserCard, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    correct = models.BooleanField(default=True)
    old_rung = models.SmallIntegerField(default=0)
    new_rung = models.SmallIntegerField(default=0)

    def rung_diff(self) -> int:
        return self.new_rung - self.old_rung
