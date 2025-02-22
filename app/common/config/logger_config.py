import os
import logging
from logging.handlers import RotatingFileHandler
import psutil
from datetime import datetime
from common.config.args_config import Config

class MemoryUsageFilter(logging.Filter):
    """
    A logging filter that adds memory usage (in MB) to log records.
    """
    def filter(self, record):
        # Get the current process's memory usage information.
        process = psutil.Process()
        mem_info = process.memory_info()
        # Convert the resident set size (RSS) from bytes to megabytes.
        record.memory_usage = mem_info.rss / (1024 * 1024)
        return True

def get_logger(name, env=None, date=None, use_case_name='default', log_to_file=True, log_directory=None):
    """
    Creates and returns a logger with optional file logging.
    This function assumes the provided log_directory already exists.
    If log_directory is None, only console logging will be used.
    
    Parameters:
        name (str): The name for the logger instance.
        env (str, optional): Environment (e.g., 'prod', 'qa'). Defaults to Config().env.lower() if not provided.
        date (str, optional): Report / Run date string to include in the log file name. If not provided, today's date is used.
        use_case_name (str, optional): Use case name to include in the log file name.
        log_to_file (bool, optional): Whether to enable logging to a file.
        log_directory (str, optional): The directory where log files will be stored. If not provided and log_to_file is True, file logging is skipped.
    
    Returns:
        logging.Logger: A logger configured with a console handler and, optionally, a rotating file handler.
    """
    # Retrieve or create a logger with the specified name.
    logger = logging.getLogger(name)
    
    # Only configure the logger if it doesn't already have handlers.
    if not logger.handlers:
        # Set the logging level to DEBUG to capture all log messages.
        logger.setLevel(logging.DEBUG)
        
        # Define the log message format, including memory usage.
        log_format = "%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s | %(lineno)d | %(memory_usage).2f MB | %(message)s"
        
        formatter = logging.Formatter(log_format)
        
        # Create a console handler for logging to the console.
        console_handler = logging.StreamHandler()
        
        console_handler.setLevel(logging.DEBUG)
        
        # Attach the MemoryUsageFilter to include memory usage information.
        console_handler.addFilter(MemoryUsageFilter())
        
        # Set the formatter for the console handler.
        console_handler.setFormatter(formatter)
        
        # Add the console handler to the logger.
        logger.addHandler(console_handler)
        
        # Set up file logging if enabled and a log directory is provided.
        if log_to_file and log_directory:
            
            # Use provided env, or fallback to Config if not provided.
            if env is None:
                env = Config().env.lower()
            
            # If no date is provided, use today's date in YYYY-MM-DD format.
            if date is None:
                date = datetime.now().strftime('%Y%m%d')
            
            # Construct the log file name.
            log_file_name = f'{use_case_name}_{env}_{Config().regime.lower()}_{date}.log'
            
            # Create a RotatingFileHandler.
            file_handler = RotatingFileHandler(
                os.path.join(log_directory, log_file_name),
                maxBytes=50 * 1024 * 1024,  # Maximum file size of 50 MB
                backupCount=5               # Up to 5 backup log files
            )

            # Set the file handler's log level to DEBUG so that it captures all messages.
            file_handler.setLevel(logging.DEBUG)
            
            # Add the MemoryUsageFilter to the file handler to include memory usage info in every log record.
            file_handler.addFilter(MemoryUsageFilter())
            
            # Apply the formatter to the file handler so that log messages adhere to the specified format.
            file_handler.setFormatter(formatter)
            
            # Attach the file handler to the logger so that log messages are written to the file.
            logger.addHandler(file_handler)
    
    # Return the configured logger.
    return logger
