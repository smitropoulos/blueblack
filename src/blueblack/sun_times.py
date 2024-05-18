from datetime import time


class SunTimes:
    def __init__(self, sunrise_time: time, sunset_time: time) -> None:
        self.sunrise_time = sunrise_time
        self.sunset_time = sunset_time

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(sunrise_time=json_data["sunrise"], sunset_time=json_data["sunset"])

    def now_is_between_sun_times(self, now: time) -> bool:
        if now >= self.sunrise_time and now <= self.sunset_time:
            return True
        return False

    def now_is_outside_sun_times(self, now: time) -> bool:
        if now > self.sunset_time or now < self.sunrise_time:
            return True
        return False
