"""Main file"""

from datetime import datetime
import time

from blueblack import fetcher
from blueblack.transitions import Transitions

from .states import State
from .local_logging import logger
from .script_runner import ScriptRunner
from .config_loading import YamlConfigLoader

if __name__ == "__main__":
    cl = YamlConfigLoader()
    cl.load_config()

    fetch = fetcher.SunTimesFetcherFromApi()
    fetch.setup(cl.lat, cl.lng)
    suntimes = fetch.fetch_sun_times()

    tr = Transitions()
    tr.setup(suntimes.sunrise_time, suntimes.sunset_time)

    time_change_limits = {
        "dayLowerLimit": 5,
        "dayUpperLimit": 9,
        "nightLowerLimit": 16,
        "nightUpperLimit": 22,
    }

    sr = ScriptRunner(ScriptRunner.default_filepath)
    while True:
        now_time = datetime.now().time()
        # check if it is time to update the sunrise, sunset times

        tr.do_transition(tr.cached_state, sr)
        # Sleep for 10 mins
        logger.debug("Sleeping now...")
        time.sleep(10 * 60)
