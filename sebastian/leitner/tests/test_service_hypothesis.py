from datetime import datetime, timedelta, timezone

from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.django import TestCase

from sebastian.leitner.models import UserCard
from sebastian.leitner.service import (
    INTERVALS,
    usercard_update_due,
    usercard_update_rung,
)

from .factories import UserCardFactory


def interval_to_timedelta(interval: tuple[float, str]) -> timedelta:
    return timedelta(**{interval[1]: interval[0]})


class TestUserCardUpdateRung(TestCase):
    @given(
        st.integers(min_value=-1, max_value=10),
        st.integers(
            min_value=0, max_value=1000 * 24 * 60 * 60
        ),  # up to 1000 days in seconds
    )
    def test_usercard_update_rung(
        self, initial_rung: int, interval_seconds: int
    ) -> None:
        user_card = UserCardFactory.create(rung=initial_rung)
        interval = timedelta(seconds=interval_seconds)

        original_rung = user_card.rung
        usercard_update_rung(user_card, interval)
        new_rung = user_card.rung

        # Assertions
        self.assertIsInstance(new_rung, int)
        self.assertGreaterEqual(new_rung, 0)
        self.assertLessEqual(new_rung, len(INTERVALS))

        # if interval is small, rung should not increase more than 1
        if interval < interval_to_timedelta(INTERVALS[0]):
            if original_rung != -1:
                self.assertLessEqual(new_rung, original_rung + 1)
            else:
                self.assertEqual(new_rung, 1)


class TestUserCardUpdateDue(TestCase):
    @given(
        st.integers(min_value=0, max_value=len(INTERVALS) - 1),
        st.integers(min_value=0, max_value=10),
        st.datetimes(
            min_value=datetime(2000, 1, 1),
            max_value=datetime(2030, 12, 31),
            timezones=st.timezones(),
        ),
    )
    def test_usercard_update_due_properties(
        self, rung: int, ease: int, now: datetime
    ) -> None:
        user_card = UserCardFactory.create(rung=rung, ease=ease)
        usercard_update_due(user_card, now=now)

        # Property 1: Due date is in the future
        self.assertGreater(user_card.due, now)

        # Property 2: Due date is within a reasonable range
        base_interval = interval_to_timedelta(INTERVALS[rung])
        # a day is added to the max interval to account for the random jitter
        max_interval = base_interval * (1.0 + (ease / 10.0)) * 1.1 + timedelta(
            days=1
        )
        self.assertLess(user_card.due, now + max_interval)
