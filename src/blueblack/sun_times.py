from datetime import time


class SunTimes:
    def __init__(self, sunrise_time: time, sunset_time: time) -> None:
        self.sunrise_time = sunrise_time
        self.sunset_time = sunset_time

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(sunrise_time=json_data["sunrise"], sunset_time=json_data["sunset"])
