"""Load configuration."""

import datetime
from abc import abstractmethod
from pathlib import Path

import xdg_base_dirs
import yaml

from .local_logging import logger
from .project import PROJECT_NAME


class ConfigLoader:
    """Load configuration file."""

    def __init__(self) -> None:
        super().__init__()

        self.lat: str
        self.lng: str
        self.timezone: str

    @abstractmethod
    def load_config(self) -> None:
        """Load configuration"""


class YamlConfigLoader(ConfigLoader):
    """Read yaml config file named config.yaml

    Attributes
    ----------
        cofnig_path: path of the config.yaml file

    """

    filename = "config.yaml"
    default_filepath = xdg_base_dirs.xdg_config_home() / PROJECT_NAME

    def __init__(self, config_path: Path = default_filepath) -> None:
        super().__init__()

        if not config_path.exists():
            msg = f"{config_path} is not a valid path. Make sure it exists. Exiting"
            raise RuntimeError(msg)

        if config_path.is_dir():
            self.config_filepath = config_path / self.filename
        else:
            self.config_filepath = config_path

        logger.info(f"Config file is {self.config_filepath}")

        if not self.config_filepath.exists():
            msg = f"No file named {self.filename} found inside {config_path}. Exiting"
            raise RuntimeError(msg)

    def load_config(self):
        with open(self.config_filepath) as file:
            configuration = yaml.safe_load(file)
        logger.info(configuration)
        super().load_config()
        self.lat = configuration["lat"]
        self.lng = configuration["lng"]
        self.timezone = configuration.get("timezone", datetime.datetime.now().tzinfo)
        self.offset_sunrise = configuration.get("offset_sunrise", "0:0:0")
        self.offset_sunset = configuration.get("offset_sunset", "0:0:0")
        return configuration
