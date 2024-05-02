"""[TODO:description]

[TODO:description]
"""

import datetime
import json
import sys
import time

import requests

from . import config_loading
from .local_logging import logger
from .script_runner import ScriptRunner


class Sunrise:
    def load_config(self, conf_loader: config_loading.ConfigLoader):
        self.configuration = conf_loader.load_config()
        self.lat = conf_loader.get_lat()
        self.lng = conf_loader.get_lng()
        self.update_days = conf_loader.get_update_days()

    def run_request(self) -> tuple[str, str]:
        """[TODO:description]

        Raises:
            RuntimeError: [TODO:throw]
            RuntimeError: [TODO:throw]

        Returns:
            [TODO:return]
        """
        global last_updated
        # curl -L https://api.sunrise-sunset.org/json\ ?lat\=38.06404\&lng\=23.79253\&tzid\=Europe/Athens\&formatted\=0 | jq '.results.sunset'
        endpoint = "https://api.sunrise-sunset.org/json"
        payload = {
            "lat": self.lat,
            "lng": self.lng,
            "formatted": "0",
            "tzid": "Europe/Athens",
        }

        r = requests.get(endpoint, payload)

        if r.status_code != 200:
            logger.critical("Error code received: {}", r.status_code)
            raise RuntimeError("Cannot get sun times, did not get 200")

        # It will return a json
        resp_body = json.loads(r.text)
        if resp_body["status"] != "OK":
            logger.critical("Error code received: {}", resp_body["status"])
            raise RuntimeError("Cannot get sun times, did not get OK")

        logger.info(resp_body)

        results = resp_body["results"]

        sunrise_time_iso8601 = results["sunrise"]
        sunset_time_iso8601 = results["sunset"]

        return (sunrise_time_iso8601, sunset_time_iso8601)

    def in_window_to_transition(self, lower_limit: int, upper_limit: int):
        # run updates between 1600 and 2200
        """Check if it current time is between lowerLimit and upperLimit"""

        local_timezone = datetime.datetime.now().tzinfo
        logger.debug(local_timezone)

        lower_datetime = datetime.time(
            hour=lower_limit, minute=0, tzinfo=local_timezone
        )
        logger.debug(lower_datetime)
        upper_datetime = datetime.time(
            hour=upper_limit, minute=0, tzinfo=local_timezone
        )
        logger.debug(upper_datetime)

        now_time = datetime.datetime.now().time()
        logger.debug(now_time)

        return now_time < upper_datetime and now_time > lower_datetime

    def time_diff(self, date_time1: datetime.datetime, date_time2: datetime.datetime):
        """[TODO:description]

        Args:
            date_time1: [TODO:description]
            date_time2: [TODO:description]
        """
        hours_diff = abs(date_time1.time().hour - date_time2.time().hour)
        mins_diff = abs(date_time1.time().minute - date_time2.time().minute)
        time_delta = datetime.timedelta(hours=hours_diff, minutes=mins_diff)
        logger.debug(f"Time_diff - {time_delta}")

    def past_time(self, l_time: datetime.datetime):
        """[TODO:description]

        Args:
            l_time: [TODO:description]

        Returns:
            [TODO:return]
        """
        return datetime.datetime.now() > l_time

    def update_sun_times(self) -> tuple[str, str]:
        # initial run - never updated
        """[TODO:description]

        Raises:
            RuntimeError: [TODO:throw]

        Returns:
            [TODO:return]
        """
        if last_updated == 0:
            return self.run_request()
        elif now - last_updated > datetime.timedelta(days=30):
            return self.run_request()
            # check if one month passed
        raise RuntimeError("Cannot update sun times")

    def give_date_times_from_req(self) -> tuple[datetime.datetime, datetime.datetime]:
        """[TODO:description]

        Returns:
            [TODO:return]
        """
        (sunrise_time_iso8601, sunset_time_iso8601) = self.run_request()
        if sunrise_time_iso8601 == "0":
            logger.critical("Error in getting the sun times. Exiting...")
            sys.exit(1)
        _sunrise_time = datetime.datetime.fromisoformat(sunrise_time_iso8601)
        _sunsset_time = datetime.datetime.fromisoformat(sunset_time_iso8601)
        return (_sunrise_time, _sunsset_time)

    def calc_sunrise_sunset_deltas(
        self,
        now_: datetime.datetime,
        sunrise: datetime.datetime,
        sunset: datetime.datetime,
    ) -> tuple[datetime.timedelta, datetime.timedelta]:
        """[TODO:description]

        Args:
            now: [TODO:description]
            sunrise: [TODO:description]
            sunset: [TODO:description]

        Returns:
            [TODO:return]
        """
        sunrise_hours_diff = abs(now_.time().hour - sunrise.time().hour)
        sunrise_mins_diff = abs(now_.time().minute - sunrise.time().minute)
        logger.debug(f"diffs - {sunrise_hours_diff}, {sunrise_mins_diff}")
        self.sunrise_delta = datetime.timedelta(
            hours=sunrise_hours_diff, minutes=sunrise_mins_diff
        )
        logger.debug(f"deltatime - {self.sunrise_delta}")

        sunset_hours_diff = abs(now_.time().hour - sunset.time().hour)
        sunset_mins_diff = abs(now_.time().minute - sunset.time().minute)
        logger.debug(f"diffs - {abs(sunset_hours_diff)}, {abs(sunset_mins_diff)}")
        self.sunset_delta = datetime.timedelta(
            hours=sunset_hours_diff, minutes=sunset_mins_diff
        )
        logger.debug(f"deltatime - {self.sunset_delta}")

        return (self.sunrise_delta, self.sunset_delta)

    def get_next_transition(self) -> str:
        """[TODO:description]

        Returns:
            [TODO:return]
        """
        if self.sunrise_delta > self.sunset_delta:
            return "sunset"
        return "sunrise"


if __name__ == "__main__":
    sn = Sunrise()
    sn.load_config(config_loading.YamlConfigLoader())
    sr = ScriptRunner()

    time_change_limits = {
        "dayLowerLimit": 5,
        "dayUpperLimit": 9,
        "nightLowerLimit": 16,
        "nightUpperLimit": 22,
    }

    CURRENT_THEME = ""

    sunrise_time, sunset_time = sn.give_date_times_from_req()
    timezone_info = sunrise_time.tzinfo
    now = last_updated = datetime.datetime.now(timezone_info)

    while True:
        # check if it is time to update the sunrise, sunset times
        now = datetime.datetime.now(timezone_info)
        if now - last_updated > datetime.timedelta(days=sn.update_days):
            sunrise_time, sunset_time = sn.give_date_times_from_req()

        # If in the window to transition to daytime
        if sn.in_window_to_transition(
            time_change_limits["dayLowerLimit"], time_change_limits["dayUpperLimit"]
        ):
            if now > sunrise_time:
                CURRENT_THEME = "light"
                logger.info("Transitioning to light")
                sr.run_scripts_in_dir("light")

        # If in the window to transition to nightimte
        if sn.in_window_to_transition(
            time_change_limits["nightLowerLimit"], time_change_limits["nightUpperLimit"]
        ):
            if now > sunset_time:
                CURRENT_THEME = "dark"
                logger.info("Transitioning to dark")
                sr.run_scripts_in_dir("dark")

        # Sleep for 10 mins
        logger.debug("Sleeping now...")
        sn.calc_sunrise_sunset_deltas(now, sunrise_time, sunset_time)
        logger.info(
            f"Next transition is{sn.get_next_transition()}.\
            Sunset in {sn.sunset_delta}, sunrise in {sn.sunrise_delta}"
        )
        time.sleep(10 * 60)
