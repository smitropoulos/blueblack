import pytest
import requests_mock
from blueblack.fetcher import SunTimesFetcherFromApi
from blueblack.datetime_utils import get_timezone_name


@pytest.fixture
def mock_api():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def get_fetcher():
    fetch = SunTimesFetcherFromApi()
    return fetch


@pytest.mark.parametrize(
    "lat,lng, fake_response_data",
    [
        (
            "10",
            "10",
            {
                "results": {
                    "sunrise": "2015-05-21T05:05:35+00:00",
                    "sunset": "2015-05-21T19:22:59+00:00",
                    "solar_noon": "2015-05-21T12:14:17+00:00",
                    "day_length": 51444,
                    "civil_twilight_begin": "2015-05-21T04:36:17+00:00",
                    "civil_twilight_end": "2015-05-21T19:52:17+00:00",
                    "nautical_twilight_begin": "2015-05-21T04:00:13+00:00",
                    "nautical_twilight_end": "2015-05-21T20:28:21+00:00",
                    "astronomical_twilight_begin": "2015-05-21T03:20:49+00:00",
                    "astronomical_twilight_end": "2015-05-21T21:07:45+00:00",
                },
                "status": "OK",
                "tzid": "UTC",
            },
        ),
    ],
)
def test_get_lat_lng_working(
    lat, lng, fake_response_data, mock_api, get_fetcher: SunTimesFetcherFromApi
):
    # Get local timezone
    tz_info = get_timezone_name()
    base_url = "https://api.example.com/json"

    mock_api.get(
        f"{base_url}?lat={lat}&lng={lng}&formatted=0&tzid={tz_info}",
        json=fake_response_data,
    )

    # Get a fetcher
    fet = get_fetcher
    fet.setup(lat, lng, base_url)

    response = fet._run_request()

    assert response.sunrise_time == fake_response_data["results"]["sunrise"]
    assert response.sunset_time == fake_response_data["results"]["sunset"]


@pytest.mark.parametrize(
    "lat,lng, fake_response_data, fake_rc",
    [
        (
            "0",
            "0",
            {
                "results": {},
                "status": "KO",
                "tzid": "UTC",
            },
            "200",
        ),
        (
            "0",
            "0",
            {},
            "404",
        ),
    ],
)
def test_get_lat_lng_failing(
    lat, lng, fake_response_data, mock_api, get_fetcher, fake_rc
):
    # Register the mock API call with the correct URL and response data

    # Get local timezone
    tz_info = get_timezone_name()
    base_url = "https://api.example.com/json"

    mock_api.get(
        f"{base_url}?lat={lat}&lng={lng}&formatted=0&tzid={tz_info}",
        json=fake_response_data,
        status_code=fake_rc,
    )

    # Get a fetcher
    fet = get_fetcher
    fet.setup(lat, lng, base_url)

    with pytest.raises(RuntimeError):
        fet._run_request()
