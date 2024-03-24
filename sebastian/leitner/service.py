from datetime import timedelta
from random import random

from django.utils import timezone

from .models import Card, Deck, Face, User, UserCard, UserCardTest

# Leitner's intervals
INTERVALS = [
    (5.0, "seconds"),
    (25.0, "seconds"),
    (2.0 * 60.0, "seconds"),
    (10.0 * 60.0, "seconds"),
    (1.0, "hours"),
    (5.0, "hours"),
    (1.0, "days"),
    (5.0, "days"),
    (25.0, "days"),
    (4.0 * 4.0, "weeks"),
    (2.0 * 52.0, "weeks"),
]


def usercard_test_correct(usercard: UserCard) -> None:
    """user got it right, so we update accordingly"""
    old_rung = usercard.rung
    q = usercard.usercardtest_set.all().order_by("-timestamp")
    if usercard.ease < 10:
        usercard.ease += 1

    if q.count() == 0:
        # never tested before. find the interval between now and
        # when the card was added which self.due should be set to
        # currently and calculate rung based on that
        now = timezone.now()
        interval = now - usercard.due
        usercard_update_rung(usercard, interval)
    else:
        # if the time since the last passed test was greater than
        # one of the intervals, make sure that it gets bumped up
        # to at least that rung
        last_correct = q[0].timestamp
        now = timezone.now()
        interval = now - last_correct
        usercard_update_rung(usercard, interval)
    UserCardTest.objects.create(
        usercard=usercard,
        correct=True,
        old_rung=old_rung,
        new_rung=usercard.rung,
    )
    usercard_update_due(usercard)


def usercard_test_wrong(usercard: UserCard) -> None:
    UserCardTest.objects.create(
        usercard=usercard, correct=False, old_rung=usercard.rung, new_rung=0
    )
    usercard.rung = 0
    usercard.ease -= 1
    if usercard.ease < 0:
        usercard.ease = 0
    usercard_update_due(usercard)


def usercard_update_rung(usercard: UserCard, interval: timedelta) -> None:
    intervals = INTERVALS[:]
    intervals.reverse()
    rung = 10
    for n, u in intervals:
        li = timedelta(**{u: n})
        if interval > li:
            # upgrade to either rung + 1 or the rung
            # that matches the interval
            usercard.rung = max(rung, usercard.rung + 1)
            break
        rung -= 1
    else:
        # tested within 5 seconds of the card being added
        if usercard.rung < 1:
            usercard.rung = 1


def usercard_update_due(usercard: UserCard) -> None:
    """figure out the next due date for this card based on rung,
    difficulty, and current datetime"""

    # if rung == -1, the user has never been presented with this card,
    # so we should never be here
    if usercard.rung == -1:
        return
    if usercard.rung > len(INTERVALS) - 1:
        usercard.rung = len(INTERVALS) - 1

    (n, u) = INTERVALS[usercard.rung]

    # extend interval based on ease. Ie, if they've gotten it right
    # 10 times out of 10, the interval gets doubled. 0 out of the last 10,
    # we stick with leitner's interval. Anything in between is proportional

    n *= 1.0 + (usercard.ease / 10.0)

    # add a 10% plus or minus to smoothe things out a bit
    n = ((n * 0.2) * random()) + (n * 0.9)  # nosec

    d = timedelta(**{u: n})
    now = timezone.now()
    usercard.due = now + d
    usercard.save()


def create_card(
    front: Face, back: Face, deck: Deck, user: User, priority: int = 1
) -> None:
    card = Card.objects.create(front=front, back=back, deck=deck)
    UserCard.objects.create(
        card=card,
        user=user,
        due=timezone.now(),
        priority=priority,
    )


def get_or_create_deck(deck_name: str, user: User) -> Deck:
    try:
        return Deck.objects.get(name=deck_name, user=user)
    except Deck.DoesNotExist:
        return Deck.objects.create(name=deck_name, user=user)


def usercard_update(
    card: UserCard, front_content: str, back_content: str, priority: int
) -> None:
    card.card.front.content = front_content
    card.card.front.save()
    card.card.back.content = back_content
    card.card.back.save()
    card.priority = priority
    card.save()
