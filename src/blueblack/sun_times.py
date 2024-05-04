class SunTimes:
    def __init__(self, lat: str, lng: str) -> None:
        self.lat = lat
        self.lng = lng

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(lat=json_data["lat"], lng=json_data["lng"])
