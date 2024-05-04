from blueblack import sun_times
import pytest


@pytest.mark.parametrize(
    "sunrise_time,sunset_time",
    [
        (
            "10",
            "100",
        ),
    ],
)
def test_sun_times(sunrise_time, sunset_time):
    st = sun_times.SunTimes(sunrise_time, sunset_time)
    assert sunrise_time == st.sunrise_time
    assert sunset_time == st.sunset_time
