from datetime import UTC, datetime
import json
from abc import abstractmethod

import requests

from .local_logging import logger
from .sun_times import SunTimes
from jsonschema import validate


class SunTimesFetcher:
    """Fetches sunrise and sunset times in UTC"""

    @abstractmethod
    def fetch_sun_times(self) -> SunTimes:
        """Get the sunsrise and sunset times for your location in UTC
        Returns: Return sunrise"""
        pass


class SunTimesFetcherFromApi(SunTimesFetcher):
    """Get sunrise/sunset times from an API call
    to default https://api.sunrise-sunset.org/json"""

    default_api_uri = "https://api.sunrise-sunset.org/json"
    expected_schema = {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "results": {
                "type": "object",
                "properties": {
                    "sunrise": {"type": "string"},
                    "sunset": {"type": "string"},
                },
                "additionalProperties": True,
                "required": ["sunrise", "sunset"],
            },
        },
        "required": ["status", "results"],
        "additionalProperties": False,
    }

    def validate_response(self, response):
        return validate(instance=response, schema=self.expected_schema)

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
        }

        r = requests.get(self.endpoint, payload, timeout=30)

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

        # These times will be in UTC. Need to adjust them for correctness
        logger.info(f"Request return {resp_body}")

        results = resp_body["results"]

        sunr = results["sunrise"]
        suns = results["sunset"]

        logger.debug(f"Sunrise returned: {sunr} - Sunset returned: {suns}")
        return SunTimes(
            datetime.fromisoformat(sunr).timetz(), datetime.fromisoformat(suns).timetz()
        )

    def _run_request(self) -> SunTimes:
        return self.run_request(self.lat, self.lng)

    def fetch_sun_times(self) -> SunTimes:
        return self._run_request()
