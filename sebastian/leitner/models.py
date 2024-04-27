from datetime import datetime
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

    def num_cards_due(self, user: User, now: Optional[datetime] = None) -> int:
        if now is None:
            now = datetime.now()
        return UserCard.objects.filter(
            user=user, rung__gte=0, card__deck=self, due__lte=now
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
