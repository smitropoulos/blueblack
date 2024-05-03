from datetime import time

from blueblack import transitions
from blueblack.states import State

sunrise_time = time(hour=7)
sunset_time = time(hour=20)

test_data = [
    {
        "now": time(hour=6),
        "sunrise": sunrise_time,
        "sunset": sunset_time,
        "expected": State.LIGHT,
    },
    {
        "now": time(hour=16),
        "sunrise": sunrise_time,
        "sunset": sunset_time,
        "expected": State.DARK,
    },
    {
        "now": time(hour=0, minute=10),
        "sunrise": sunrise_time,
        "sunset": sunset_time,
        "expected": State.LIGHT,
    },
    {
        "now": time(hour=23, minute=59),
        "sunrise": sunrise_time,
        "sunset": sunset_time,
        "expected": State.LIGHT,
    },
    {
        "now": time(hour=7),
        "sunrise": sunrise_time,
        "sunset": sunset_time,
        "expected": State.DARK,
    },
]

trans = transitions.Transition()


def test_transition_setup(tmp_path):
    """Transition cache file tests"""
    trans.setup(tmp_path)


def test_calc_next_transition():
    for entry in test_data:
        print(entry)
        assert (
            trans.calc_next_transition(entry["sunrise"], entry["sunset"], entry["now"])
            == entry["expected"]
        )
