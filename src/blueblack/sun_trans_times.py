import json
from abc import abstractmethod
from datetime import datetime

import requests

from .local_logging import logger
from .datetime_utils import get_timezone_name


class SunTimesFetcher:
    """docstring for SunTimesFetcher."""

    @abstractmethod
    def fetch_sun_times(self, parameter_list) -> tuple[datetime, datetime, datetime]:
        """Get the sunsrise and sunset times for your location
        Args:
            parameter_list ([TODO:parameter]): [TODO:description]

        Returns: Return sunrise, sunset, and time updated

        """
        pass


class SunTimesFetcherFromApi(SunTimesFetcher):
    """Get sunrise/sunset times from an API call
    to https://api.sunrise-sunset.org/json"""

    def __init__(self, lat: str, lng: str) -> None:
        super().__init__()
        self.lat = lat
        self.lng = lng
        self.endpoint = "https://api.sunrise-sunset.org/json"

        tzname = get_timezone_name()

        if tzname is not None:
            self.timezone_name = tzname
            logger.debug(f"Timezone name is {tzname}")
        else:
            logger.critical("Could not automatically get timezone name")

    def run_request(self, endpoint: str = "") -> tuple[datetime, datetime]:
        """[TODO:description]

        Raises:
            RuntimeError: [TODO:throw]
            RuntimeError: [TODO:throw]

        Returns:
            [TODO:return]
        """

        if endpoint != "":
            self.endpoint = endpoint

        payload = {
            "lat": self.lat,
            "lng": self.lng,
            "formatted": "0",
            "tzid": self.timezone_name,
        }

        r = requests.get(self.endpoint, payload)

        if r.status_code != 200:
            logger.critical("Error code received: {}", r.status_code)
            raise RuntimeError(
                f"Cannot get sun times, did not get 200. Got {r.status_code}"
            )

        # It will return a json
        resp_body = json.loads(r.text)
        if resp_body["status"] != "OK":
            logger.critical("Error code received: {}", resp_body["status"])
            raise RuntimeError("Cannot get sun times, did not get OK")

        logger.info(f"Request return {resp_body}")

        results = resp_body["results"]

        # Current endpoint will return iso8601 formatted datetimes
        sunrise_time_iso8601 = results["sunrise"]
        sunset_time_iso8601 = results["sunset"]

        return (
            datetime.fromisoformat(sunrise_time_iso8601),
            datetime.fromisoformat(sunset_time_iso8601),
        )

    def fetch_sun_times(
        self, parameter_list=None
    ) -> tuple[datetime, datetime, datetime]:
        toret = self.run_request()
        toret = toret + (datetime.now(),)
        return toret
