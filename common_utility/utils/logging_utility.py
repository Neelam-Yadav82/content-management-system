import logging
import colorlog
import os
from django.conf import settings

# from call_audit.settings.base import BASE_DIR
BASE_DIR = settings.BASE_DIR
# Define the logs directory
logs_dir = os.path.join(BASE_DIR, "logs")
os.makedirs(logs_dir, exist_ok=True)

# Create a logger object
logger = logging.getLogger(__name__)

# Create a formatter with a colored output format
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)

# Create a StreamHandler to output to console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Add the StreamHandler to the logger
logger.addHandler(stream_handler)

# Create a FileHandler to output both successful responses and errors to the error log
error_handler = logging.FileHandler(os.path.join(logs_dir, "error.log"))
error_handler.setLevel(logging.INFO)  # Log errors and above
error_handler.setFormatter(formatter)

# Add the Error FileHandler to the logger
logger.addHandler(error_handler)

# Create a FileHandler to output exceptions to the exception log
exception_handler = logging.FileHandler(os.path.join(logs_dir, "exception.log"))
exception_handler.setLevel(logging.ERROR)  # Log exceptions and above
exception_handler.setFormatter(formatter)

# Add the Exception FileHandler to the logger
logger.addHandler(exception_handler)

# Set the log level
logger.setLevel(logging.DEBUG)  # Set your desired log level

# Disable propagation to prevent duplicate logging
logger.propagate = False
