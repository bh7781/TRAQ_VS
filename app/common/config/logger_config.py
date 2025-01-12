import os
import logging
from logging.handlers import RotatingFileHandler
import psutil
from common.config.args_config import Config
from diagnostic_pandq.output_filepath import get_output_location


class MemoryUsageFilter(logging.Filter):
    def filter(self, record):
        process = psutil.Process()
        mem_info = process.memory_info()
        record.memory_usage = mem_info.rss / (1024 * 1024)  # Convert bytes to MB
        return True


def get_logger(name, env=None, date=None, use_case_name='default', log_to_file=True):
    """
    Creates a logger with optional file logging. By default, logs only to files.
    """

    # Create a logger with the specified name
    logger = logging.getLogger(name)

    # If the logger does not have any handlers (meaning it's newly created), add handlers
    if not logger.handlers:
        # Set the overall logging level of the logger to DEBUG
        logger.setLevel(logging.DEBUG)

        # Create the format of the log message, including memory usage
        log_format = "%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s | %(lineno)d | %(memory_usage).2f MB | %(message)s"
        formatter = logging.Formatter(log_format)

        # Create a console handler that logs messages to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Add the MemoryUsageFilter to the console handler
        console_handler.addFilter(MemoryUsageFilter())

        # Set the formatter for the console handler
        console_handler.setFormatter(formatter)

        # Add the console handler to the logger
        logger.addHandler(console_handler)

        # If log_to_file is True, set up file logging
        if log_to_file:
            # Use default env and date if not provided
            if env is None:
                env = Config().env.lower()
            if date is None:
                date = 'default_date'  # Use default value or fetch current date

            # Define the log directory path based on the provided environment
            log_directory = get_output_location(env=env).get('log_files_location')

            # Create the log directory if it doesn't exist
            # if not os.path.exists(log_directory):
            #     os.makedirs(log_directory, exist_ok=True)

            # Set up the log file handler with rotation (50MB per file, up to 5 backups)
            log_file_name = f'{use_case_name}_{env}_{Config().regime.lower()}_{date}.log'
            file_handler = RotatingFileHandler(
                os.path.join(log_directory, log_file_name),
                maxBytes=50 * 1024 * 1024,
                backupCount=5
            )

            # Set the logging level of the file handler to DEBUG
            file_handler.setLevel(logging.DEBUG)

            # Add the MemoryUsageFilter to the file handler
            file_handler.addFilter(MemoryUsageFilter())

            # Set the formatter for the file handler
            file_handler.setFormatter(formatter)

            # Add the file handler to the logger
            logger.addHandler(file_handler)

    # Return the configured logger
    return logger
