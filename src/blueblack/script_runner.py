import subprocess
import xdg_base_dirs
import os
from local_logging import logger


class script_runner:
    default_filepath = xdg_base_dirs.xdg_config_home().__str__() + "/sunrise"

    def __init__(self, scripts_path: str = "") -> None:
        if not (scripts_path is None or scripts_path) == "":
            self.scripts_path = scripts_path
        else:
            self.scripts_path = self.default_filepath

    def get_dir(self, transition_to: str):
        return self.scripts_path + "/" + transition_to + "_mode"

    def run_scripts_in_dir(self, transition_to: str):
        if transition_to not in ["light", "dark"]:
            raise Exception(f"No can do transition to {transition_to}")
        dir = self.get_dir(transition_to)
        logger.info(f"Running scripts in {dir}")
        for filename in os.listdir(dir):
            f = os.path.join(dir, filename)
            # checking if it is a file
            if os.path.isfile(f):
                if os.access(f, os.X_OK):
                    output = subprocess.run(f, capture_output=True, timeout=10)
                    if output.returncode != 0:
                        logger.error(
                            f"File {f} returned error code {output.returncode}"
                        )
                else:
                    logger.error(f"File {f} is not executable")


if __name__ == "__main__":
    sr = script_runner()
    sr.run_scripts_in_dir("dark")
