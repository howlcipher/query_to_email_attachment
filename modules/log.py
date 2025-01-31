import logging
import os
from datetime import datetime

def setup_logging(log_dir, log_prefix):
    """
    Setup logging configuration.

    Args:
    - log_dir (str): Directory path where log files will be stored.
    - log_prefix (str): Prefix to prepend to log file names.

    Returns:
    - None
    """
    if not logging.getLogger().hasHandlers():
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_filename = f"{log_prefix}_{datetime.now().strftime('%Y-%m-%d')}.log"
        log_filepath = os.path.join(log_dir, log_filename)

        logging.basicConfig(
            filename=log_filepath,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

def log(message):
    """
    Log a message with a timestamp.

    Args:
    - message (str): Message to be logged.

    Returns:
    - None
    """
    print(message)
    logging.info(message)

# Example usage if running log.py directly
if __name__ == "__main__":
    log("Testing logging")
