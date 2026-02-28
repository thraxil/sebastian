from datetime import datetime

from django.contrib.auth.models import User
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.django import TestCase

from sebastian.leitner.selectors import due_range

from .factories import UserCardFactory


class TestDueRange(TestCase):
    @given(
        lower=st.datetimes(
            min_value=datetime(2000, 1, 1),
            max_value=datetime(2030, 12, 31),
            timezones=st.timezones(),
        ),
        upper=st.datetimes(
            min_value=datetime(2000, 1, 1),
            max_value=datetime(2030, 12, 31),
            timezones=st.timezones(),
        ),
        data=st.data(),
    )
    def test_due_range_properties(
        self, lower: datetime, upper: datetime, data
    ) -> None:
        # Ensure we have a user to associate with UserCards
        user = User.objects.create(username="testuser")

        # Create some UserCards with due dates potentially within the range
        # For simplicity, create a fixed number of cards for now.
        # A more advanced test might generate a variable number and distribution of cards.
        for _ in range(10):
            # Ensure due dates are within a reasonable range for testing
            UserCardFactory.create(
                user=user,
                due=data.draw(
                    st.datetimes(
                        min_value=datetime(1990, 1, 1),
                        max_value=datetime(2040, 12, 31),
                        timezones=st.just(
                            lower.tzinfo if lower.tzinfo else None
                        ),
                    )
                ),
            )

        # Call the function under test
        count = due_range(user, lower, upper)

        # Property 1: The count should be non-negative
        self.assertGreaterEqual(count, 0)

        # Property 2: If lower > upper, the count should be 0
        if lower > upper:
            self.assertEqual(count, 0)

        # Property 3: The count should be correct by manually filtering
        expected_count = UserCardFactory._meta.model.objects.filter(
            user=user,
            rung__gte=0,
            due__lte=upper,
            due__gte=lower,
        ).count()
        self.assertEqual(count, expected_count)
