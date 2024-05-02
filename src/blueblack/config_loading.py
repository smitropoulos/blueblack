from abc import abstractmethod
from pathlib import Path
import xdg_base_dirs
from local_logging import logger
import yaml


class config_loader:
    @abstractmethod
    def load_config(self):
        pass

    @abstractmethod
    def get_lat(self) -> str:
        pass

    @abstractmethod
    def get_lng(self) -> str:
        pass

    @abstractmethod
    def get_update_days(self) -> int:
        pass


class yaml_config_loader(config_loader):
    """Read yaml config file named config.yaml

    Attributes:
        cofnig_path: path of the config.yaml file
    """

    filename = "config.yaml"
    default_filepath = xdg_base_dirs.xdg_config_home().__str__() + "/sunrise"

    def __init__(self, config_path: str = default_filepath) -> None:
        super().__init__()

        config_loc = Path(config_path)

        if not config_loc.exists():
            raise RuntimeError(f"{config_path} is not a valid path. Exiting")

        if config_loc.is_dir():
            self.config_filepath = config_loc / self.filename
        else:
            self.config_filepath = config_loc

        logger.info(f"Config file is {self.config_filepath}")

        if not self.config_filepath.exists():
            raise RuntimeError(
                f"No file named {self.filename} found inside {config_path}. Exiting"
            )

    def load_config(self):
        with open(self.config_filepath, "r") as file:
            configuration = yaml.safe_load(file)
        logger.info(configuration)
        super().load_config()
        self.lat = configuration["lat"]
        self.lng = configuration["lng"]
        self.update_days = configuration["update_days"]
        return configuration

    def get_lat(self) -> str:
        return self.lat

    def get_lng(self) -> str:
        return self.lng

    def get_update_days(self) -> int:
        return self.update_days
