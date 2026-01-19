import factory
from django.contrib.auth.models import User
from django.utils import timezone

from sebastian.leitner.models import Card, Deck, Face, UserCard


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Sequence(lambda n: "user%d@example.com" % n)


class FaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Face

    content = factory.Sequence(lambda n: "Face %d" % n)


class DeckFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Deck

    name = factory.Sequence(lambda n: "Deck %d" % n)
    user = factory.SubFactory(UserFactory)


class CardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Card

    front = factory.SubFactory(FaceFactory)
    back = factory.SubFactory(FaceFactory)
    deck = factory.SubFactory(DeckFactory)


class UserCardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserCard

    user = factory.SubFactory(UserFactory)
    card = factory.SubFactory(CardFactory)
    due = factory.LazyFunction(timezone.now)
