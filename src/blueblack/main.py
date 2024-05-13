"""Main file"""

import time
from datetime import datetime

from blueblack import suntimes_fetcher
from blueblack.states import State
from blueblack.transitions import Transitions

from .config_loading import YamlConfigLoader
from .local_logging import logger
from .script_runner import ScriptRunner

if __name__ == "__main__":
    yaml_config_loader = YamlConfigLoader()
    yaml_config_loader.load_config()

    suntimes_fetcher = suntimes_fetcher.SunTimesFetcherFromApi()
    suntimes_fetcher.setup(yaml_config_loader.lat, yaml_config_loader.lng)
    suntimes = suntimes_fetcher.fetch_sun_times()

    transition = Transitions()
    transition.setup(suntimes.sunrise_time, suntimes.sunset_time)

    script_runner = ScriptRunner(ScriptRunner.default_filepath)

    last_transition = None

    while True:
        now_time = datetime.now().time()
        # check if it is time to update the sunrise, sunset times

        next_transition = transition.calc_next(
            suntimes.sunset_time, suntimes.sunset_time
        )
        if last_transition != next_transition:
            if next_transition == State.DARK:
                if now_time > suntimes.sunset_time:
                    transition.execute(next_transition, script_runner)
                    last_transition = State.DARK

            if next_transition == State.LIGHT:
                if now_time > suntimes.sunrise_time:
                    transition.execute(next_transition, script_runner)
                    last_transition = State.LIGHT

        logger.debug("Sleeping now...")
        time.sleep(5)
