from blueblack import sun_times
from datetime import time
import pytest


@pytest.mark.parametrize(
    "sunrise_time,sunset_time",
    [
        (
            time(10),
            time(18),
        ),
    ],
)
def test_sun_times(sunrise_time, sunset_time):
    st = sun_times.SunTimes(sunrise_time, sunset_time)
    assert sunrise_time == st.sunrise_time
    assert sunset_time == st.sunset_time


@pytest.mark.parametrize(
    "sunrise_time,sunset_time, now_time, expected",
    [
        (time(10), time(18), time(14), True),
        (time(10), time(18), time(20), False),
        (time(4), time(4), time(4), True),
    ],
)
def test_now_is_between_sun_times(sunrise_time, sunset_time, now_time, expected):
    st = sun_times.SunTimes(sunrise_time, sunset_time)
    if expected:
        assert st.now_is_between_sun_times(now_time)
    else:
        assert not st.now_is_between_sun_times(now_time)


@pytest.mark.parametrize(
    "sunrise_time,sunset_time, now_time, expected",
    [
        (time(10), time(18), time(14), False),
        (time(10), time(18), time(20), True),
        (time(4), time(4), time(4), False),
    ],
)
def test_now_is_outside_sun_times(sunrise_time, sunset_time, now_time, expected):
    st = sun_times.SunTimes(sunrise_time, sunset_time)
    if expected:
        assert st.now_is_outside_sun_times(now_time)
    else:
        assert not st.now_is_outside_sun_times(now_time)
