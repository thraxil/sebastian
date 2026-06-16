from datetime import datetime, timedelta, timezone

from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.django import TestCase

from sebastian.leitner.models import Card, UserCard
from sebastian.leitner.service import (
    INTERVALS,
    usercard_update_due,
    usercard_update_rung,
)

from .factories import DeckFactory, FaceFactory, UserCardFactory, UserFactory


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


from hypothesis.stateful import RuleBasedStateMachine, initialize, rule

from sebastian.leitner import service


class UserCardLifecycle(RuleBasedStateMachine):
    @initialize(rung=st.integers(-1, 10), ease=st.integers(0, 10))
    def init_card(self, rung: int, ease: int) -> None:
        self.card = UserCardFactory.create(rung=rung, ease=ease)

    @rule(
        now=st.datetimes(
            min_value=datetime(2000, 1, 1),
            max_value=datetime(2030, 12, 31),
            timezones=st.timezones(),
        )
    )
    def test_correct(self, now: datetime) -> None:
        old_rung = self.card.rung
        old_ease = self.card.ease

        service.usercard_test_correct(self.card, now=now)

        self.card.refresh_from_db()
        # Invariants
        if old_rung != -1:
            assert self.card.rung >= old_rung
        assert self.card.ease >= old_ease
        assert self.card.due > now

    @rule(
        now=st.datetimes(
            min_value=datetime(2000, 1, 1),
            max_value=datetime(2030, 12, 31),
            timezones=st.timezones(),
        )
    )
    def test_wrong(self, now: datetime) -> None:
        old_ease = self.card.ease
        service.usercard_test_wrong(self.card, now=now)

        self.card.refresh_from_db()
        # Invariants
        assert self.card.rung == 0
        if old_ease > 0:
            assert self.card.ease == old_ease - 1
        else:
            assert self.card.ease == 0
        assert self.card.due > now


TestUserCardLifecycle = UserCardLifecycle.TestCase


class TestUserCardUpdateProperties(TestCase):
    @given(
        front_content=st.text(),
        back_content=st.text(),
        priority=st.integers(
            min_value=0, max_value=32767
        ),  # PositiveSmallIntegerField bounds
    )
    def test_usercard_update_properties(
        self, front_content: str, back_content: str, priority: int
    ) -> None:
        uc = UserCardFactory()
        service.usercard_update(
            card=uc,
            front_content=front_content,
            back_content=back_content,
            priority=priority,
        )
        uc.refresh_from_db()
        self.assertEqual(uc.card.front.content, front_content)
        self.assertEqual(uc.card.back.content, back_content)
        self.assertEqual(uc.priority, priority)


class TestCreateCardProperties(TestCase):
    @given(
        priority=st.integers(min_value=0, max_value=32767),
        now=st.datetimes(
            min_value=datetime(2000, 1, 1),
            max_value=datetime(2030, 12, 31),
            timezones=st.timezones(),
        ),
    )
    def test_create_card_properties(
        self, priority: int, now: datetime
    ) -> None:
        f = FaceFactory()
        b = FaceFactory()
        d = DeckFactory()
        u = d.user

        service.create_card(
            front=f, back=b, deck=d, user=u, priority=priority, now=now
        )

        c = Card.objects.get(front=f, back=b, deck=d)
        uc = UserCard.objects.get(card=c, user=u)

        self.assertEqual(uc.priority, priority)
        self.assertEqual(uc.due, now)
        self.assertEqual(uc.rung, -1)
        self.assertEqual(uc.ease, 5)


class TestDeckProperties(TestCase):
    @given(deck_name=st.text(min_size=1, max_size=256))
    def test_get_or_create_deck_properties(self, deck_name: str) -> None:
        u = UserFactory()

        # Test creation
        deck1 = service.get_or_create_deck(deck_name, u)
        self.assertEqual(deck1.name, deck_name)
        self.assertEqual(deck1.user, u)

        # Test getting
        deck2 = service.get_or_create_deck(deck_name, u)
        self.assertEqual(deck1.id, deck2.id)
