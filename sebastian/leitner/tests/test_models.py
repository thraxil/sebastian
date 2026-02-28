from django.test import TestCase
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.django import TestCase as DjangoTestCase

from ..models import Face
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


class TestFaceHypothesis(DjangoTestCase):
    @given(st.text(min_size=1, max_size=1000))
    def test_face_size_properties(self, content: str) -> None:
        f = Face(content=content)
        size = f.size()

        # Property 1: size is a float
        self.assertIsInstance(size, float)

        # Property 2: size is within the defined bounds [16, 200]
        self.assertGreaterEqual(size, 16.0)
        self.assertLessEqual(size, 200.0)

        # Property 3: size calculation logic
        expected_size = 800 / len(content)
        if expected_size < 16:
            self.assertEqual(size, 16.0)
        elif expected_size > 200:
            self.assertEqual(size, 200.0)
        else:
            self.assertEqual(size, expected_size)
