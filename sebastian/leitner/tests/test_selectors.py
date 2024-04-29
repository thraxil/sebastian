from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ..selectors import (
    closest_due_card,
    due_range,
    ease_stats,
    first_deck_due,
    first_due,
    first_due_deck_card,
    next_card,
    next_day_due,
    next_deck_card,
    next_hour_due,
    next_month_due,
    next_six_hours_due,
    next_week_due,
    random_untested_card,
    random_untested_from_priority,
    recent_tests,
    rungs_stats,
    total_deck_due,
    total_due,
    total_tested,
    total_untested,
    user_decks,
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

    def test_next_six_hours_due(self) -> None:
        u = UserFactory()
        self.assertEqual(next_six_hours_due(u), 0)

    def test_next_day_due(self) -> None:
        u = UserFactory()
        self.assertEqual(next_day_due(u), 0)

    def test_next_week_due(self) -> None:
        u = UserFactory()
        self.assertEqual(next_week_due(u), 0)

    def test_next_month_due(self) -> None:
        u = UserFactory()
        self.assertEqual(next_month_due(u), 0)

    def test_user_decks(self) -> None:
        u = UserFactory()
        self.assertEqual(user_decks(u).count(), 0)

    def test_next_card(self) -> None:
        u = UserFactory()
        self.assertIsNone(next_card(u))

    def test_closest_due_card(self) -> None:
        u = UserFactory()
        self.assertIsNone(closest_due_card(u))

    def test_random_untested_card(self) -> None:
        u = UserFactory()
        self.assertIsNone(random_untested_card(u))

    def test_random_untested_from_priority(self) -> None:
        u = UserFactory()
        self.assertIsNone(random_untested_from_priority(u, 1))

    def test_first_due(self) -> None:
        u = UserFactory()
        self.assertIsNone(first_due(u))

    def test_first_deck_due(self) -> None:
        d = DeckFactory()
        u = d.user
        self.assertIsNone(first_deck_due(u, d))

    def test_recent_tests(self) -> None:
        u = UserFactory()
        self.assertEqual(recent_tests(u).count(), 0)

    def test_next_deck_card(self) -> None:
        d = DeckFactory()
        u = d.user
        self.assertIsNone(next_deck_card(u, d))

    def test_first_due_deck_card(self) -> None:
        d = DeckFactory()
        u = d.user
        self.assertIsNone(first_due_deck_card(u, d))
