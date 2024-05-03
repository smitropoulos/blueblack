"""Transition to sunrise or sunset"""

from datetime import datetime, time
from pathlib import Path

import xdg_base_dirs

from .local_logging import logger
from .script_runner import ScriptRunner
from .states import State

Default_Cache_dir = xdg_base_dirs.xdg_cache_home()
Default_Cache_subdir = "blueblack"
Default_cache_filename = "cached_state"


class Transition:
    """Handle transition between State's"""

    def setup(self, cache_dir_path: Path = Default_Cache_dir):
        """Setup the transitions cache

        Args:
            cache_dir_path: where should the cache be?
        """
        self.cache_dirpath = cache_dir_path / Default_Cache_subdir
        self.cache_filepath = self.cache_dirpath / Default_cache_filename
        logger.info("Trying to read state from the file")

        # Create parent dirs and file
        self.cache_filepath.parent.mkdir(parents=True, exist_ok=True)
        self.cache_filepath.touch()
        contents = self.cache_filepath.read_text()

        if contents == "light":
            self.cached_state = State.LIGHT
            logger.info("Read light mode")
        elif contents == "dark":
            self.cached_state = State.DARK
            logger.info("Read dark mode")
        else:
            logger.warning("Could not determine initial state. Will guess")

    def calc_next_transition(
        self,
        sunrise_time: time,
        sunset_time: time,
        time_now: time = datetime.now().time(),
    ) -> State:
        """Calculate the next transition by this logic:
        if e.g. it is 1530 now, the sunrise time was 0700, and the sunset time is 1900
        then the next transition is dark

        Args:
            sunrise_time: sunrise time
            time_now: the time now

        Returns:
            The next state calculated
        """
        logger.debug(
            f"Getting next transition with now time: {time_now} and sunrise time: {sunrise_time} "
        )
        if time_now >= sunrise_time and time_now < sunset_time:
            return State.DARK

        return State.LIGHT

    def transition(self, st: State, runner: ScriptRunner):
        if st == State.LIGHT:
            runner.run_scripts_in_dir("light")
        else:
            runner.run_scripts_in_dir("dark")
