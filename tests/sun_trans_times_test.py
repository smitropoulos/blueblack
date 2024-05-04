import pytest
import requests_mock
from blueblack import fetcher

lat = "100"
lng = "100"


@pytest.fixture
def mock_api():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def user_repository(mock_api):
    base_url = "https://api.example.com"
    repo = fetcher.SunTimesFetcherFromApi(lat, lng, base_url)
    return repo


def test_init():
    fetc = fetcher.SunTimesFetcherFromApi(lat, lng)
    assert fetc.lat == lat
    assert fetc.lng == lng
