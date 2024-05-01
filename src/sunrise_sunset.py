import datetime
import json
import time
from local_logging import logger

import requests

import config_loading
from script_runner import script_runner


class sunrise:
    def load_config(self, conf_loader: config_loading.config_loader):
        self.configuration = conf_loader.load_config()
        self.lat = conf_loader.get_lat()
        self.lng = conf_loader.get_lng()
        self.update_days = conf_loader.get_update_days()

    def run_request(self) -> tuple[str, str]:
        global last_updated
        # curl -L https://api.sunrise-sunset.org/json\?lat\=38.06404\&lng\=23.79253\&tzid\=Europe/Athens\&formatted\=0 | jq '.results.sunset'
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

    def in_window_to_transition(self, lowerLimit: int, upperLimit: int):
        # run updates between 1600 and 2200
        """Check if it current time is between lowerLimit and upperLimit"""

        local_timezone = datetime.datetime.now().tzinfo
        logger.debug(local_timezone)

        lowerDatetime = datetime.time(hour=lowerLimit, minute=0, tzinfo=local_timezone)
        logger.debug(lowerDatetime)
        upperDatetime = datetime.time(hour=upperLimit, minute=0, tzinfo=local_timezone)
        logger.debug(upperDatetime)

        now_time = datetime.datetime.now().time()
        logger.debug(now_time)

        return now_time < upperDatetime and now_time > lowerDatetime

    def past_time(self, time: datetime.datetime):
        return datetime.datetime.now() > time

    def update_sun_times(self) -> tuple[str, str]:
        # initial run - never updated
        if last_updated == 0:
            return self.run_request()
        elif now - last_updated > datetime.timedelta(days=30):
            return self.run_request()
            # check if one month passed
        raise RuntimeError("Cannot update sun times")

    def give_date_times_from_req(self) -> tuple[datetime.datetime, datetime.datetime]:
        (sunrise_time_iso8601, sunset_time_iso8601) = self.run_request()
        if sunrise_time_iso8601 == "0":
            logger.critical("Error in getting the sun times. Exiting...")
            exit(1)
        sunrise_time = datetime.datetime.fromisoformat(sunrise_time_iso8601)
        sunsset_time = datetime.datetime.fromisoformat(sunset_time_iso8601)
        return (sunrise_time, sunsset_time)

    def calc_sunrise_sunset_deltas(
        self,
        now: datetime.datetime,
        sunrise: datetime.datetime,
        sunset: datetime.datetime,
    ) -> tuple[datetime.timedelta, datetime.timedelta]:
        sunrise_hours_diff = abs(now.time().hour - sunrise.time().hour)
        sunrise_mins_diff = abs(now.time().minute - sunrise.time().minute)
        logger.debug(f"diffs - {sunrise_hours_diff}, {sunrise_mins_diff}")
        self.sunrise_delta = datetime.timedelta(
            hours=sunrise_hours_diff, minutes=sunrise_mins_diff
        )
        logger.debug(f"deltatime - {self.sunrise_delta}")

        sunset_hours_diff = abs(now.time().hour - sunset.time().hour)
        sunset_mins_diff = abs(now.time().minute - sunset.time().minute)
        logger.debug(f"diffs - {abs(sunset_hours_diff)}, {abs(sunset_mins_diff)}")
        self.sunset_delta = datetime.timedelta(
            hours=sunset_hours_diff, minutes=sunset_mins_diff
        )
        logger.debug(f"deltatime - {self.sunset_delta}")

        return (self.sunrise_delta, self.sunset_delta)

    def get_next_transition(self) -> str:
        if self.sunrise_delta > self.sunset_delta:
            return "sunset"
        return "sunrise"


if __name__ == "__main__":
    sn = sunrise()
    sn.load_config(config_loading.yaml_config_loader())
    sr = script_runner()

    time_change_limits = {
        "dayLowerLimit": 5,
        "dayUpperLimit": 9,
        "nightLowerLimit": 16,
        "nightUpperLimit": 22,
    }

    current_theme = ""

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
                current_theme = "light"
                logger.info("Transitioning to light")
                sr.run_scripts_in_dir("light")

        # If in the window to transition to nightimte
        if sn.in_window_to_transition(
            time_change_limits["nightLowerLimit"], time_change_limits["nightUpperLimit"]
        ):
            if now > sunset_time:
                current_theme = "dark"
                logger.info("Transitioning to dark")
                sr.run_scripts_in_dir("dark")

        # Sleep for 10 mins
        logger.debug("Sleeping now...")
        sn.calc_sunrise_sunset_deltas(now, sunrise_time, sunset_time)
        logger.info(
            f"Next transition is {sn.get_next_transition()}. Sunset in {sn.sunset_delta}, sunrise in {sn.sunrise_delta}"
        )
        time.sleep(10 * 60)
