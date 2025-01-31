import sqlalchemy as sa
from sqlalchemy.engine.url import URL
import pandas as pd
from .log import log

class DatabaseHandler:
    def __init__(self, config):
        self.server = config['server']
        self.database = config['database']
        self.username = config['login']['username']
        self.password = config['login']['password']
        self.connection = None

    def __enter__(self):
        try:
            connection_url = URL.create(
                "mssql+pyodbc",
                username=self.username,
                password=self.password,
                host=self.server,
                database=self.database,
                query={"driver": "ODBC Driver 17 for SQL Server"}
            )
            self.engine = sa.create_engine(connection_url)
            self.connection = self.engine.connect()
            log("Successfully connected to the database.")
            return self
        except Exception as e:
            log(f"Error connecting to database: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
            log("Database connection closed.")

    def execute_query(self, query):
        try:
            df = pd.read_sql_query(query, self.connection)
            log(f"Successfully executed query: {query}")
            return df
        except Exception as e:
            log(f"Error executing query: {e}")
            return None
