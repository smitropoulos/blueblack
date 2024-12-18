"""
    Resolver:

    Required:
        datetime (from python)
        astral (from python-astral)
        sun_times (from the project)

    Exported:
        class TimeResolver:
            This class is used to resolve sunrise & sunset time.

            constructor(lat: string, lng: string, timezone: string, offsetSunrise: string, offsetSunset: string) -> TimeResolver:
                store data.
            
            calculate(latitude: string, longitude: string, timezone: string, offsetSunrise: string, offsetSunset: string) -> SunTimes:
                Calculate with specific data (not stored data).

            resolve() -> SunTimes:
                apply stored data to this.calculate() and return.
"""

from datetime import datetime as Datetime, timedelta

from astral import LocationInfo
from astral.sun import sun

from .sun_times import SunTimes

class TimeResolver:
    """
        get sunrist/sunset times from python astral, renamed and removed useless jump functions
    """

    def __init__(self, lat: str, lng: str, timezone:str, offsetSunrise: str, offsetSunset: str):
        self.lat = lat
        self.lng = lng
        self.timezone = timezone
        self.offsetSunrise = offsetSunrise
        self.offsetSunset = offsetSunset

    def calculate(self, latitude: str, longitude: str, timezone: str, offsetSunrise: str, offsetSunset: str) -> SunTimes:
        city = LocationInfo('name','region', timezone, latitude, longitude)
        s = sun(city.observer, Datetime.today(), tzinfo=timezone)

        # parse string to list[int]
        offsetSunriseTimes = list(map(int,offsetSunrise.split(":")))
        offsetSunsetTimes = list(map(int,offsetSunset.split(":")))

        # ensure the length is correct
        offsetSunriseTimes.extend([0]*(3-len(offsetSunriseTimes)))
        offsetSunsetTimes.extend([0]*(3-len(offsetSunsetTimes)))

        return SunTimes(
            (s["sunrise"]+timedelta(hours=offsetSunriseTimes[0],minutes=offsetSunriseTimes[1],seconds=offsetSunriseTimes[2])).time(),
            (s["sunset"]+timedelta(hours=offsetSunsetTimes[0],minutes=offsetSunsetTimes[1],seconds=offsetSunsetTimes[2])).time(),
        )
    
    def resolve(self):
        return self.calculate(self.lat,self.lng,self.timezone,self.offsetSunrise,self.offsetSunset)