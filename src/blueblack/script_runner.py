"""Run scripts inside a dir"""

import os
from pathlib import Path
import subprocess

import xdg_base_dirs
import xdg_base_dirs

from blueblack import project

from .local_logging import logger
from .states import State


class ScriptRunner:
    """Run scripts inside a dir

    Attributes:
        default_filepath: Default directory to run scripts in
        defaults to ~/.config/blueblack/{dark,light}_mode if xdg_config_home is defined
    """

    default_filepath = xdg_base_dirs.xdg_config_home() / project.PROJECT_NAME

    def __init__(self, scripts_path: Path) -> None:
        self.scripts_path = scripts_path

    def get_dir(self, to_mode: State):
        """Return the default dir filepath according to next transition

        Args:
            transition_to: next transition

        Returns:
            Retrurn the complete path
        """
        if to_mode == State.DARK:
            return self.scripts_path / Path("dark_mode")
        elif to_mode == State.LIGHT:
            return self.scripts_path / Path("light_mode")

    def run_scripts_in_dir(self, transition_to: State):
        """Run scripts inside the default dir

        Args:
            transition_to: next transition ["light"|"dark"]
        """
        directory = self.get_dir(transition_to)
        if not directory.exists() or not directory.is_dir():
            logger.error(f"{directory} does not exist. Will not run anything")
            return
        logger.info(f"Running scripts in {directory}")
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                if os.access(f, os.X_OK):
                    output = subprocess.run(
                        f, capture_output=True, timeout=10, check=False
                    )
                    if output.returncode != 0:
                        logger.error(
                            f"File {f} returned error code {output.returncode}"
                        )
                else:
                    logger.warn(f"File {f} is not executable")
