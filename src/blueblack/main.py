"""Main file."""

import time
from datetime import datetime

from blueblack.config_loading import YamlConfigLoader
from blueblack.local_logging import logger
from blueblack.script_runner import ScriptRunner
from blueblack.states import State
from blueblack.transitions import Transitions

from blueblack.resolver import TimeResolver

if __name__ == "__main__":
    yaml_config_loader = YamlConfigLoader()
    yaml_config_loader.load_config()

    resolver = TimeResolver(yaml_config_loader.lat, yaml_config_loader.lng, yaml_config_loader.timezone, yaml_config_loader.offset_sunrise, yaml_config_loader.offset_sunset)

    suntimes = resolver.resolve()

    transition = Transitions()

    script_runner = ScriptRunner(ScriptRunner.default_filepath)

    seconds_in_day = 86400
    sleep_interval = 5

    while True:
        now_time = datetime.now().timetz()

        next_transition = transition.calc_next(
            suntimes.sunrise_time,
            suntimes.sunset_time,
            now_time,
        )

        # Apply opposite here
        if transition.last_transition is None or transition.last_transition == next_transition:
            logger.debug(
                "Skipped a transition or new execution."
                f"Will apply opposite of {next_transition}",
            )
            if next_transition == State.DARK:
                transition.execute(State.LIGHT, script_runner)
            else:
                transition.execute(State.DARK, script_runner)

        elif transition.last_transition != next_transition:
            # check if we are past the time for a transition
            if next_transition == State.DARK and suntimes.now_is_outside_sun_times(now_time):
                transition.execute(State.DARK, script_runner)

            if next_transition == State.LIGHT and suntimes.now_is_between_sun_times(now_time):
                transition.execute(State.LIGHT, script_runner)

        logger.debug("Sleeping now...")
        time.sleep(sleep_interval)
