"""Transition to sunrise or sunset"""

from datetime import datetime, time
from os import path

import xdg_base_dirs

from .local_logging import logger
from .script_runner import ScriptRunner
from .states import State

DEF_CACHE_DIR = str(xdg_base_dirs.xdg_cache_home()) + "/blueblack"
DEF_CACHE_FILE = path.join(DEF_CACHE_DIR, "cached_state")


class Transition:
    """Handle transition between State's"""

    def __init__(self) -> None:
        self.cache_file = DEF_CACHE_FILE
        if path.exists(DEF_CACHE_FILE):
            with open(self.cache_file, "rw") as file:
                contents = file.readline()
                if contents == "light":
                    self.cached_state = State.LIGHT
                elif contents == "dark":
                    self.cached_state = State.DARK
                else:
                    logger.warn("Could not determine initial state. Will guess")


    def calc_next_transition(
        self, sunrise_time: time, time_now: time = datetime.now().time()
    ) -> State:

        logger.debug(
            f"Getting next transition with now time: {time_now} and sunrise time: {sunrise_time} "
        )
        if time_now > sunrise_time:
            return State.DARK
        else:
            return State.LIGHT

    def transition(self, st: State, runner: ScriptRunner):
        if st == State.LIGHT:
            runner.run_scripts_in_dir("light")
        else:
            runner.run_scripts_in_dir("dark")
