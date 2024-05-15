"""Main file"""

import time
from datetime import UTC, datetime

from blueblack import suntimes_fetcher
from blueblack.config_loading import YamlConfigLoader
from blueblack.local_logging import logger
from blueblack.script_runner import ScriptRunner
from blueblack.states import State
from blueblack.transitions import Transitions

if __name__ == "__main__":
    yaml_config_loader = YamlConfigLoader()
    yaml_config_loader.load_config()

    suntimes_fetcher = suntimes_fetcher.SunTimesFetcherFromApi()
    suntimes_fetcher.setup(yaml_config_loader.lat, yaml_config_loader.lng)
    suntimes = suntimes_fetcher.fetch_sun_times()

    transition = Transitions()

    script_runner = ScriptRunner(ScriptRunner.default_filepath)

    seconds_in_day = 86400
    sleep_interval = 5
    seconds_rem = seconds_in_day * yaml_config_loader.update_days

    while True:
        now_time = datetime.now(UTC).timetz()

        next_transition = transition.calc_next(
            suntimes.sunrise_time, suntimes.sunset_time, now_time
        )

        # Apply opposite here
        if (
            transition.last_transition is None
            or transition.last_transition == next_transition
        ):
            logger.debug(
                f"Skipped a transition or new execution. Will apply opposite of {next_transition}"
            )
            if next_transition == State.DARK:
                transition.execute(State.LIGHT, script_runner)
            else:
                transition.execute(State.DARK, script_runner)

        elif transition.last_transition != next_transition:
            # check if we are past the time for a transition
            if next_transition == State.DARK:
                if now_time > suntimes.sunset_time or now_time < suntimes.sunrise_time:
                    transition.execute(State.DARK, script_runner)
            if next_transition == State.LIGHT:
                if now_time > suntimes.sunrise_time and now_time < suntimes.sunset_time:
                    transition.execute(State.LIGHT, script_runner)

        # check if it is time to update the sunrise, sunset times
        if seconds_rem <= 0:
            suntimes = suntimes_fetcher.fetch_sun_times()
            seconds_rem = seconds_in_day
        else:
            seconds_rem = seconds_rem - sleep_interval

        logger.debug("Sleeping now...")
        time.sleep(sleep_interval)
