import json
from abc import abstractmethod

import requests

from .local_logging import logger
from .datetime_utils import get_timezone_name
from .sun_times import SunTimes


class SunTimesFetcher:
    """docstring for SunTimesFetcher."""

    @abstractmethod
    def fetch_sun_times(self) -> SunTimes:
        """Get the sunsrise and sunset times for your location
        Returns: Return sunrise, sunset, and time updated"""
        pass


class SunTimesFetcherFromApi(SunTimesFetcher):
    """Get sunrise/sunset times from an API call
    to default https://api.sunrise-sunset.org/json"""

    default_api_uri = "https://api.sunrise-sunset.org/json"

    def __init__(self) -> None:
        super().__init__()
        tzname = get_timezone_name()

        if tzname is not None:
            self.timezone_name = tzname
            logger.debug(f"Timezone name is {tzname}")
        else:
            logger.critical("Could not automatically get timezone name")

    def setup(self, lat: str, lng: str, endpoint: str = default_api_uri):
        self.endpoint = endpoint
        self.lat = lat
        self.lng = lng

    def run_request(self, lat: str, lng: str) -> SunTimes:
        """Run a get request to the endpoint

        Raises:
            RuntimeError: for not 200 responses
            RuntimeError: for not OK responses from the API

        Returns:
            Returns a dict with keys:
            ["sunrise"]
            ["sunset"]
            They include datetimes for sunrise and sunset datetimes
        """

        payload = {
            "lat": lat,
            "lng": lng,
            "formatted": "0",
            "tzid": self.timezone_name,
        }

        r = requests.get(self.endpoint, payload)

        if r.status_code != 200:
            logger.critical(f"Error code received: {r.status_code}")
            raise RuntimeError(
                f"Cannot get sun times, did not get 200. Got {r.status_code}"
            )

        # It will return a json
        resp_body = json.loads(r.text)
        if resp_body["status"] != "OK":
            logger.critical(f"Error code received: {resp_body["status"]}")
            raise RuntimeError("Cannot get sun times, did not get OK")

        logger.info(f"Request return {resp_body}")

        results = resp_body["results"]

        return SunTimes(results["sunrise"], results["sunset"])

    def _run_request(self) -> SunTimes:
        return self.run_request(self.lat, self.lng)

    def fetch_sun_times(self) -> SunTimes:
        return self._run_request()
