from enum import Enum


class State(Enum):
    LIGHT = 0
    DARK = 1

def determine_current_state() -> State:
    return State.LIGHT
