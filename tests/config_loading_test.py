import shutil

import pytest
import yaml
from blueblack.config_loading import YamlConfigLoader


@pytest.mark.parametrize(
    "yaml_dict",
    [
        {
            "lat": 20.2003,
            "lng": 33.1233,
            "update_days": 3,
        },
        {
            "lat": -1,
            "lng": 0,
            "update_days": 30000,
        },
    ],
)
def test_load_conf(temporary_path, yaml_dict):
    out = {}
    with open(temporary_path / YamlConfigLoader.filename, "w") as file:
        yaml.dump(yaml_dict, file, default_flow_style=False)

    with open(temporary_path / YamlConfigLoader.filename, "r") as file:
        out = yaml.safe_load(file)

    assert yaml_dict == out

    cl = YamlConfigLoader(temporary_path)
    cl.load_config()


@pytest.fixture(scope="module")
def temporary_path(tmp_path_factory):
    my_tmpdir = tmp_path_factory.mktemp("config")
    my_tmpdir.chmod(0o777)
    yield my_tmpdir
    shutil.rmtree(my_tmpdir)
