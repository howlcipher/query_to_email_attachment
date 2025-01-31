import pandas as pd
import os
from datetime import datetime
from .log import log

class ExcelSaver:
    def __init__(self, save_directory, csv_filename):
        """
        Initialize the ExcelSaver with directory and filename settings.

        Args:
        - save_directory (str): Directory where the Excel file will be saved.
        - csv_filename (str): Desired filename for the Excel file.
        """
        self.save_directory = save_directory
        self.csv_filename = csv_filename

    def save(self, query_results):
        """
        Save query results to an Excel file with multiple sheets.

        Args:
        - query_results (dict): Dictionary where keys are sheet names and values are Pandas DataFrames.

        Returns:
        - str: Filepath of the saved Excel file.

        Raises:
        - Exception: If there is an error during the file saving process.
        """
        try:
            # Ensure the directory exists
            if not os.path.exists(self.save_directory):
                os.makedirs(self.save_directory)

            # Create a timestamped filename
            timestamp = datetime.now().strftime("%Y-%m-%d")
            filename = f"{self.csv_filename.split('.')[0]}_{timestamp}.xlsx"
            filepath = os.path.join(self.save_directory, filename)

            # Create a Pandas Excel writer using XlsxWriter as the engine
            with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
                for sheet_name, df in query_results.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

            log(f"Successfully saved query results to {filepath}")

            return filepath  # Return the filepath for potential use elsewhere
        except Exception as e:
            log(f"Error saving to Excel file: {e}")
            raise
