import os
import shutil
from datetime import datetime, timedelta
from modules.log import log  # Assuming log function is imported from modules.log

class FileCleaner:
    def __init__(self, directory, days_old=30):
        """
        Initialize FileCleaner with directory path and days_old threshold.

        Args:
        - directory (str): Directory path to clean up.
        - days_old (int, optional): Number of days old for files to be considered for deletion. Default is 30.
        """
        self.directory = directory
        self.days_old = days_old

    def cleanup(self):
        """
        Delete files older than specified days in the given directory.
        """
        if os.path.exists(self.directory):
            for filename in os.listdir(self.directory):
                file_path = os.path.join(self.directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        file_age = datetime.now() - datetime.fromtimestamp(os.path.getctime(file_path))
                        if file_age > timedelta(days=self.days_old):
                            os.unlink(file_path)
                            log(f"Deleted old file: {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        log(f"Deleted directory: {file_path}")
                except Exception as e:
                    log(f'Failed to delete {file_path}. Reason: {e}')

def cleanup_directory(directory, days_old=30):
    """
    Convenience function to clean up files using FileCleaner.

    Args:
    - directory (str): Directory path to clean up.
    - days_old (int, optional): Number of days old for files to be considered for deletion. Default is 30.
    """
    cleaner = FileCleaner(directory, days_old)
    cleaner.cleanup()
