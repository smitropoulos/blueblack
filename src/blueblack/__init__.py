# read version from installed package
from importlib.metadata import version
from .project import PROJECT_NAME

__version__ = version(PROJECT_NAME)
