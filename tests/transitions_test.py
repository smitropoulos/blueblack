from datetime import time
import pytest

from blueblack.transitions import Transition
from blueblack.states import State


@pytest.fixture
def get_sunrise():
    return time(hour=7)


@pytest.fixture
def get_sunset():
    return time(hour=19)


@pytest.fixture
def get_transition():
    trans = Transition()
    return trans


def test_transition_setup(get_transition, tmp_path):
    """Transition cache file tests"""
    trans = get_transition
    trans.setup(tmp_path)


@pytest.mark.parametrize(
    "now, expected",
    [
        (
            time(hour=7),
            State.DARK,
        ),
        (
            time(hour=6),
            State.LIGHT,
        ),
        (
            time(hour=16),
            State.DARK,
        ),
        (
            time(hour=0, minute=10),
            State.LIGHT,
        ),
        (
            time(hour=23, minute=59),
            State.LIGHT,
        ),
    ],
)
def test_calc_next_transition(get_transition, now, get_sunrise, get_sunset, expected):
    trans = get_transition
    exp = trans.calc_next_transition(get_sunrise, get_sunset, now)
    assert exp == expected
