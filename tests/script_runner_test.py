from pathlib import Path
import pytest
from blueblack import script_runner
from blueblack.states import State


@pytest.mark.parametrize(
    "mode, expected",
    [
        (State.LIGHT, "light_mode"),
        (State.DARK, "dark_mode"),
    ],
)
def test_get_dir(mode, tmp_path, expected):
    sr = script_runner.ScriptRunner(tmp_path)
    exp_path = Path(tmp_path / Path(expected))
    assert sr.get_dir(mode) == exp_path
