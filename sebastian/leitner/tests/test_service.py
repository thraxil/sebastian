from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone

from sebastian.leitner import service
from sebastian.leitner.models import Card, UserCard
from sebastian.leitner.tests.factories import (
    CardFactory,
    DeckFactory,
    FaceFactory,
    UserCardFactory,
    UserFactory,
)


class ServiceTests(TestCase):
    def test_get_or_create_deck_gets(self):
        d = DeckFactory()
        deck = service.get_or_create_deck(d.name, d.user)
        self.assertEqual(deck.id, d.id)

    def test_get_or_create_deck_creates(self):
        u = UserFactory()
        deck_name = "new deck"
        deck = service.get_or_create_deck(deck_name, u)
        self.assertEqual(deck.name, deck_name)
        self.assertEqual(deck.user.id, u.id)

    def test_create_card(self):
        f = FaceFactory()
        b = FaceFactory()
        d = DeckFactory()
        u = UserFactory()
        now = datetime(2023, 9, 25, 12, 0, 0, tzinfo=timezone.UTC)

        service.create_card(
            front=f, back=b, deck=d, user=u, priority=10, now=now
        )

        c = Card.objects.get(front=f, back=b, deck=d)
        uc = UserCard.objects.get(card=c, user=u)
        self.assertEqual(uc.priority, 10)
        self.assertEqual(uc.due, now)

    def test_usercard_update(self):
        uc = UserCardFactory()
        service.usercard_update(
            card=uc,
            front_content="new front",
            back_content="new back",
            priority=12,
        )
        self.assertEqual(uc.card.front.content, "new front")
        self.assertEqual(uc.card.back.content, "new back")
        self.assertEqual(uc.priority, 12)

    def test_usercard_update_due(self):
        now = datetime(2023, 9, 25, 12, 0, 0, tzinfo=timezone.UTC)
        uc = UserCardFactory(rung=0)
        service.usercard_update_due(usercard=uc, now=now)
        # n is 5 seconds. gets a 10% fuzz
        self.assertGreaterEqual(uc.due, now + timedelta(seconds=6.75))
        self.assertLessEqual(uc.due, now + timedelta(seconds=8.25))

    def test_usercard_update_due_with_ease(self):
        now = datetime(2023, 9, 25, 12, 0, 0, tzinfo=timezone.UTC)
        uc = UserCardFactory(rung=0, ease=10)
        service.usercard_update_due(usercard=uc, now=now)
        # n is 5 seconds. gets doubled because of ease
        # and then a 10% fuzz
        self.assertGreaterEqual(uc.due, now + timedelta(seconds=9))
        self.assertLessEqual(uc.due, now + timedelta(seconds=11))

    def test_usercard_update_rung(self):
        uc = UserCardFactory(rung=0)
        service.usercard_update_rung(uc, timedelta(days=6))
        self.assertEqual(uc.rung, 7)

    def test_usercard_test_wrong(self):
        now = datetime(2023, 9, 25, 12, 0, 0, tzinfo=timezone.UTC)
        uc = UserCardFactory(rung=5, ease=5)
        service.usercard_test_wrong(uc, now=now)
        self.assertEqual(uc.rung, 0)
        self.assertEqual(uc.ease, 4)
        # due should be updated
        self.assertGreater(uc.due, now)

    def test_usercard_test_correct_first_test(self):
        now = datetime(2023, 9, 25, 12, 0, 0, tzinfo=timezone.UTC)
        due = now - timedelta(days=1)
        uc = UserCardFactory(rung=-1, due=due)
        service.usercard_test_correct(uc, now=now)
        self.assertEqual(uc.rung, 5)
        self.assertEqual(uc.ease, 6)
        self.assertGreater(uc.due, now)

    def test_usercard_test_correct_retest(self):
        now = datetime(2023, 9, 25, 12, 0, 0, tzinfo=timezone.UTC)
        uc = UserCardFactory(rung=2, due=now - timedelta(days=1))
        service.usercard_test_correct(uc, now=now)
        self.assertGreater(uc.rung, 2)
