from django.test import TestCase

from .factories import CardFactory, DeckFactory, FaceFactory


class TestFace(TestCase):
    def test_face(self) -> None:
        f = FaceFactory()
        self.assertTrue(133 < f.size() < 140)


class TestDeck(TestCase):
    def test_empty_deck(self) -> None:
        d = DeckFactory()
        self.assertEqual(d.num_cards(), 0)
        self.assertEqual(d.num_cards_due(d.user), 0)
        self.assertEqual(d.num_unlearned(d.user), 0)


class TestCard(TestCase):
    def test_card(self) -> None:
        c = CardFactory()
        self.assertEqual(c.deck.num_cards(), 1)
