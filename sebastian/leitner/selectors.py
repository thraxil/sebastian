from typing import Generator

from django.contrib.auth.models import User
from django.utils import timezone

from .models import Deck, UserCard


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
