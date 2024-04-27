from django.test import TestCase

from ..selectors import (
    ease_stats,
    rungs_stats,
    total_deck_due,
    total_due,
    total_tested,
    total_untested,
    user_percent_right,
    user_priority_stats,
)
from .factories import DeckFactory, UserFactory


class TestEmptyDeck(TestCase):
    def test_rungs_stats(self):
        u = UserFactory()
        r = list(rungs_stats(u))
        for i in range(10):
            self.assertEqual(r[i], {"rung": i, "cards": 0})

    def test_ease_stats(self):
        u = UserFactory()
        r = list(ease_stats(u))
        for i in range(10):
            self.assertEqual(r[i], {"ease": i, "cards": 0})

    def test_total_tested(self):
        u = UserFactory()
        self.assertEqual(total_tested(u), 0)

    def test_total_untested(self):
        u = UserFactory()
        self.assertEqual(total_untested(u), 0)

    def test_total_due(self):
        u = UserFactory()
        self.assertEqual(total_due(u), 0)

    def test_total_deck_due(self):
        d = DeckFactory()
        self.assertEqual(total_deck_due(d.user, d), 0)

    def test_user_percent_right(self):
        u = UserFactory()
        self.assertEqual(user_percent_right(u), 0.0)

    def test_user_priority_stats(self):
        u = UserFactory()
        r = list(user_priority_stats(u))
        for i in range(10):
            self.assertEqual(
                r[i], {"priority": 10 - i, "tested": 0, "untested": 0}
            )
