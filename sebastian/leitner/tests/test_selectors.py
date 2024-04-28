from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ..selectors import (
    due_range,
    ease_stats,
    next_hour_due,
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
    def test_rungs_stats(self) -> None:
        u = UserFactory()
        r = list(rungs_stats(u))
        for i in range(10):
            self.assertEqual(r[i], {"rung": i, "cards": 0})

    def test_ease_stats(self) -> None:
        u = UserFactory()
        r = list(ease_stats(u))
        for i in range(10):
            self.assertEqual(r[i], {"ease": i, "cards": 0})

    def test_total_tested(self) -> None:
        u = UserFactory()
        self.assertEqual(total_tested(u), 0)

    def test_total_untested(self) -> None:
        u = UserFactory()
        self.assertEqual(total_untested(u), 0)

    def test_total_due(self) -> None:
        u = UserFactory()
        self.assertEqual(total_due(u), 0)

    def test_total_deck_due(self) -> None:
        d = DeckFactory()
        self.assertEqual(total_deck_due(d.user, d), 0)

    def test_user_percent_right(self) -> None:
        u = UserFactory()
        self.assertEqual(user_percent_right(u), 0.0)

    def test_user_priority_stats(self) -> None:
        u = UserFactory()
        r = list(user_priority_stats(u))
        for i in range(10):
            self.assertEqual(
                r[i], {"priority": 10 - i, "tested": 0, "untested": 0}
            )

    def test_due_range(self) -> None:
        u = UserFactory()
        lower = timezone.now()
        upper = lower + timedelta(hours=1)
        self.assertEqual(due_range(u, lower, upper), 0)

    def test_next_hour_due(self) -> None:
        u = UserFactory()
        self.assertEqual(next_hour_due(u), 0)
