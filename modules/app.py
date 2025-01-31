from modules.query import DatabaseHandler
from modules.save_query_to_csv import ExcelSaver
from modules.email import EmailSender
from modules.log import setup_logging
from modules.config_loader import ConfigLoader
from modules.file_cleaner import FileCleaner
import pandas as pd

class MainApp:
    def __init__(self, config_path):
        self.config_loader = ConfigLoader(config_path)
        self.config = self.config_loader.load()
        setup_logging(self.config['log_file']['directory'], self.config['log_file']['filename_prefix'])
    
    def run_queries(self):
        query_results = {}
        with DatabaseHandler(self.config) as db_handler:
            for query_info in self.config['queries']:
                query = query_info['query']
                sheet_name = query_info['sheet_name']
                df = db_handler.execute_query(query)
                if df is not None:
                    query_results[sheet_name] = df
        return query_results

    def save_results(self, query_results):
        save_directory = self.config.get('csv_directory', 'output_files')
        csv_filename = self.config['csv_filename']
        excel_saver = ExcelSaver(save_directory, csv_filename)
        return excel_saver.save(query_results)

    def check_if_data_exists(self, filepath):
        """
        Check if the Excel file contains any data beyond headers.
        
        Args:
        - filepath (str): Path to the Excel file.
        
        Returns:
        - bool: True if data exists, False otherwise.
        """
        xls = pd.ExcelFile(filepath)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            if not df.empty:
                return True
        return False

    def send_email(self, filepath):
        query_results = self.run_queries()  # Get the query results
        email_sender = EmailSender(self.config)
        
        if email_sender.attachment:
            email_sender.attachment_source = filepath
            if not self.check_if_data_exists(filepath):
                email_sender.body = "No results returned."

        # Pass query_results to send_email
        email_sender.send_email(query_results)  # Pass query_results here


    def clean_up_files(self):
        if self.config.get('cleanup', {}).get('enabled', False):
            cleanup_config = self.config['cleanup']
            cleaner = FileCleaner(cleanup_config['directory'], cleanup_config['days_old'])
            cleaner.cleanup()

    def run(self):
        query_results = self.run_queries()
        filepath = self.save_results(query_results)
        self.send_email(filepath)
        self.clean_up_files()

# Example usage:
if __name__ == "__main__":
    config_path = 'path/to/your/config.json'
    app = MainApp(config_path)
    app.run()
