import re

from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.django import TestCase

from sebastian.hashcolor import _adjust, color, luminosity, make_contrasting


class TestColor(TestCase):
    @given(st.text())
    def test_color_returns_valid_hex(self, phrase: str) -> None:
        # Act
        result = color(phrase)

        # Assert
        assert re.match(r"^[0-9a-f]{6}$", result) is not None


class TestAdjust(TestCase):
    @given(
        st.floats(min_value=0, max_value=255)
        | st.integers(min_value=0, max_value=255)
    )
    def test_adjust_properties(self, value: float | int) -> None:
        result = _adjust(value)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)


class TestLuminosity(TestCase):
    @given(
        st.floats(min_value=0, max_value=255)
        | st.integers(min_value=0, max_value=255),
        st.floats(min_value=0, max_value=255)
        | st.integers(min_value=0, max_value=255),
        st.floats(min_value=0, max_value=255)
        | st.integers(min_value=0, max_value=255),
    )
    def test_luminosity_properties(
        self, r: float | int, g: float | int, b: float | int
    ) -> None:
        result = luminosity(r, g, b)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    def test_luminosity_known_values(self) -> None:
        self.assertAlmostEqual(luminosity(0, 0, 0), 0.0)
        self.assertAlmostEqual(luminosity(255, 255, 255), 1.0)


class TestMakeContrasting(TestCase):
    @given(
        st.tuples(
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
        )
    )
    def test_make_contrasting_tuple_input(
        self, color_tuple: tuple[int, int, int]
    ) -> None:
        result = make_contrasting(color_tuple)
        self.assertIn(result, [(0, 0, 0), (255, 255, 255)])

    @given(
        st.builds(
            lambda s: "".join(s),
            st.lists(
                st.sampled_from("0123456789abcdef"), min_size=6, max_size=6
            ),
        )
    )
    def test_make_contrasting_string_input(self, color_string: str) -> None:
        result = make_contrasting(color_string)
        self.assertIn(result, [(0, 0, 0), (255, 255, 255)])
