from abc import abstractmethod
from datetime import datetime

from astral import LocationInfo
from astral.sun import sun

from .sun_times import SunTimes

class SunTimesFetcher:
    """Fetches sunrise and sunset times in current timezone."""

    @abstractmethod
    def fetch_sun_times(self) -> SunTimes:
        """Get the sunsrise and sunset times for your location in current timezone
        Returns: Return sunrise
        """


class SunTimesFetcherFromApi(SunTimesFetcher):
    """
        get sunrist/sunset times from python astral
    """

    def setup(self, lat: str, lng: str, timezone:str):
        self.lat = lat
        self.lng = lng
        self.timezone = timezone

    def calculate(self, latitudeString: str, longitudeString: str, timezoneString: str) -> SunTimes:
        city = LocationInfo('name','region', timezoneString, latitudeString, longitudeString)
        s = sun(city.observer, datetime.today(), tzinfo=timezoneString)
        return SunTimes(
            s["sunrise"].time(),
            s["sunset"].time()
        )

    def _run_request(self) -> SunTimes:
        result = self.calculate(self.lat, self.lng, self.timezone)
        return result

    def fetch_sun_times(self) -> SunTimes:
        return self._run_request()
