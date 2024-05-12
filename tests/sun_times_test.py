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
