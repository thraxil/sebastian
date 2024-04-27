from datetime import timedelta
from random import randint
from typing import Generator, Optional

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.utils import timezone

from .models import Deck, UserCard, UserCardTest


def rungs_stats(user: User) -> Generator[dict, None, None]:
    # TODO: convert to more efficient sql query
    d = dict()
    for x in range(-1, 11):
        d[x] = 0

    for uc in UserCard.objects.filter(user=user, rung__gte=0):
        d[uc.rung] = d[uc.rung] + 1

    for i in range(11):
        yield dict(rung=i, cards=d[i])


def ease_stats(user: User) -> Generator[dict, None, None]:
    # TODO: convert to more efficient sql query
    d = dict()
    for x in range(-1, 11):
        d[x] = 0

    for uc in UserCard.objects.filter(user=user, rung__gte=0):
        d[uc.ease] = d[uc.ease] + 1

    for i in range(11):
        yield dict(ease=i, cards=d[i])


def total_tested(user: User) -> int:
    return UserCard.objects.filter(user=user, rung__gte=0).count()


def total_untested(user: User) -> int:
    return UserCard.objects.filter(user=user, rung=-1).count()


def total_due(user: User) -> int:
    return UserCard.objects.filter(
        user=user, rung__gte=0, due__lte=timezone.now()
    ).count()


def total_deck_due(user: User, deck: Deck) -> int:
    return UserCard.objects.filter(
        user=user, rung__gte=0, card__deck=deck, due__lte=timezone.now()
    ).count()


def user_percent_right(user: User) -> float:
    """returns percentage right for user"""
    total = UserCardTest.objects.filter(usercard__user=user).count()
    if total == 0:
        return 0.0
    right = UserCardTest.objects.filter(
        usercard__user=user, correct=True
    ).count()
    return float(right) / float(total) * 100.0


def user_priority_stats(user: User):
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
        due__lte=timezone.now() + timedelta(hours=1),
        due__gte=timezone.now(),
    ).count()


def next_day_due(user: User) -> int:
    return UserCard.objects.filter(
        user=user,
        rung__gte=0,
        due__lte=timezone.now() + timedelta(days=1),
        due__gte=timezone.now() + timedelta(hours=6),
    ).count()


def next_six_hours_due(user: User) -> int:
    return UserCard.objects.filter(
        user=user,
        rung__gte=0,
        due__lte=timezone.now() + timedelta(hours=6),
        due__gte=timezone.now() + timedelta(hours=1),
    ).count()


def next_week_due(user: User) -> int:
    return UserCard.objects.filter(
        user=user,
        rung__gte=0,
        due__lte=timezone.now() + timedelta(weeks=1),
        due__gte=timezone.now() + timedelta(days=1),
    ).count()


def next_month_due(user: User) -> int:
    return UserCard.objects.filter(
        user=user,
        rung__gte=0,
        due__lte=timezone.now() + timedelta(weeks=4),
        due__gte=timezone.now() + timedelta(weeks=1),
    ).count()


def user_decks(user: User) -> QuerySet[Deck]:
    return Deck.objects.filter(user=user)


def next_card(user: User) -> Optional["UserCard"]:
    card = closest_due_card(user)
    if card is None:
        card = random_untested_card(user)
    return card


def closest_due_card(user: User) -> Optional["UserCard"]:
    r = UserCard.objects.filter(
        user=user, due__lte=timezone.now(), rung__gte=0
    ).order_by("due")
    if r.count() > 0:
        now = timezone.now()
        alldue = list(r)
        alldue.sort(key=lambda x: abs(x.due - now))
        return alldue[0]
    else:
        return None


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


def random_untested_from_priority(
    user: User, priority: int
) -> Optional["UserCard"]:
    r = UserCard.objects.filter(user=user, rung=-1, priority=priority)
    c = r.count()
    if c > 0:
        return r[randint(0, c - 1)]  # nosec
    # no untested cards
    return None


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


def next_deck_card(user: User, deck: Deck) -> Optional["UserCard"]:
    card = first_due_deck_card(user, deck)
    if card is None:
        card = random_untested_deck_card(user, deck)
    return card


def first_due_deck_card(user: User, deck: Deck) -> Optional["UserCard"]:
    return (
        UserCard.objects.filter(
            user=user, card__deck=deck, due__lte=timezone.now(), rung__gte=0
        )
        .order_by("due")
        .first()
    )


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
