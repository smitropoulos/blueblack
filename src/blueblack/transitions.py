"""Transition to sunrise or sunset"""

from datetime import time

import xdg_base_dirs

from .local_logging import logger
from .project import PROJECT_NAME
from .script_runner import ScriptRunner
from .states import State

Default_Cache_dir = xdg_base_dirs.xdg_cache_home()
Default_Cache_subdir = PROJECT_NAME
Default_cache_filename = "cached_state"


class Transitions:
    """Handle transition between State's"""

    last_transition = None

    def calc_next(
        self,
        sunrise_time: time,
        sunset_time: time,
        time_now: time,
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
            f"Getting next transition with now time: {time_now}, sunrise time: {sunrise_time}, sunset time: {sunset_time}"
        )
        if time_now >= sunrise_time and time_now < sunset_time:
            logger.debug("Returning Dark")
            return State.DARK

        logger.debug("Returning Light")
        return State.LIGHT

    def execute(self, st: State, runner: ScriptRunner):
        runner.run_scripts_in_dir(st)
        self.update_last_transition(st)

    def update_last_transition(self, st: State):
        self.last_transition = st
