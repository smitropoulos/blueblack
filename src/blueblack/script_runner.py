"""Run scripts inside a dir"""

import os
import subprocess

import xdg_base_dirs

from .local_logging import logger


class ScriptRunner:
    """Run scripts inside a dir

    Attributes:
        default_filepath: Default directory to run scripts in
    """

    default_filepath = str(xdg_base_dirs.xdg_config_home()) + "/sunrise"

    def __init__(self, scripts_path: str = "") -> None:
        if not (scripts_path is None or scripts_path) == "":
            self.scripts_path = scripts_path
        else:
            self.scripts_path = self.default_filepath

    def get_dir(self, transition_to: str):
        """Return the default dir filepath according to next transition

        Args:
            transition_to: next transition

        Returns:
            Retrurn the complete path
        """
        return self.scripts_path + "/" + transition_to + "_mode"

    def run_scripts_in_dir(self, transition_to: str):
        """Run scripts inside the default dir

        Args:
            transition_to: next transition ["light"|"dark"]
        """
        if transition_to not in ["light", "dark"]:
            raise KeyError(f"No can do transition to {transition_to}")
        directory = self.get_dir(transition_to)
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
                    logger.error(f"File {f} is not executable")


if __name__ == "__main__":
    sr = ScriptRunner()
    sr.run_scripts_in_dir("dark")
