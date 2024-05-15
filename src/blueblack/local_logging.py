"""Logging configuration"""

import logging

logger = logging
FORMAT = "[{asctime:<20} {filename:>20}:{lineno:<4} - {funcName:<20}]   {message}"
logging.basicConfig(format=FORMAT, level=logging.DEBUG, style="{")
