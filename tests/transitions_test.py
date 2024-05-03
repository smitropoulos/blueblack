from datetime import time

from blueblack import transitions
from blueblack.states import State

trans = transitions.Transition()


sunrise_time = time(hour=7)
test_data = [
    {"now": time(hour=6), "sunrise": sunrise_time, "expected": State.LIGHT},
    {"now": time(hour=16), "sunrise": sunrise_time, "expected": State.DARK},
    {"now": time(hour=0, minute=10), "sunrise": sunrise_time, "expected": State.LIGHT},
    # {"now": time(hour=23, minute=59), "sunrise": sunrise_time, "expected": State.LIGHT},
    # {"now": time(hour=7), "sunrise": sunrise_time, "expected": State.DARK},
]


def test_calc_next_transition():
    for entry in test_data:
        print(entry)
        assert (
            trans.calc_next_transition(entry["sunrise"], entry["now"])
            == entry["expected"]
        )
