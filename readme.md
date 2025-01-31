# Database Query to CSV Export and Email Notification
This Python project connects to a database (Microsoft SQL Server or SQLite), executes a query, exports the query results to a CSV file, logs the process, and sends an email with optional CSV attachment.

## Features
- Connects to a database (MS SQL Server or SQLite).
- Executes a SELECT query specified in config.json.
- Saves query results to a CSV file.
- Logs operations and errors to a log file.
- Sends an email notification with optional CSV attachment.

## Setup
#### Prerequisites
- Python 3.x installed
- pip install -r requirements.txt
## Configuration
Clone the repository:
    
    git clone <repository-url>
    cd <repository-directory>

## Configure 
config.json:
    
    Update config.json with your database and email server details.
    {
    "server": "your_database_server",
    "database": "your_database_name",
    "login": {
        "username": "your_database_username",
        "password": "your_database_password"
    },
    "csv_directory": "output_files",
    "csv_filename": "query_results.xlsx",
    "log_file": {
        "directory": "logs",
        "filename_prefix": "db_log"
    },
    "queries": [
        {
            "sheet_name": "All Rows",
            "query": "SELECT * FROM your_table WHERE date_column = CAST(GETDATE() AS DATE);"
        },
        {
            "sheet_name": "Successes",
            "query": "SELECT * FROM your_table WHERE status = 'Success' AND date_column = CAST(GETDATE() AS DATE);"
        },
        {
            "sheet_name": "Failures",
            "query": "SELECT * FROM your_table WHERE status = 'Failure' AND date_column = CAST(GETDATE() AS DATE);"
        }
    ],
    "email": {
        "smtp_server": "your_smtp_server",
        "smtp_port": 25,
        "smtp_timeout": "200000",
        "sender_email": "your_sender_email@example.com",
        "sender_password": "your_sender_password",
        "recipient_email": "recipient@example.com",
        "subject": "Database Query Results",
        "body": "Please find the attached query results.",
        "empty_attachment_body": "Zero cases for today.",
        "attachment": true,
        "attachment_source": "",
        "smtp_auth_required": "1"
    },
    "cleanup": {
        "enabled": true,
        "directory": "output_files",
        "days_old": 30
    }
}


## Usage
Run the script main.py:

    python main.py

## Build    
    pip install pyinstaller
    pyinstaller main.spec

## Logs:
    
    Logs are stored in the logs directory with filenames like db_log_<date>.log.
## Output:

- CSV file with query results is saved as per csv_filename in config.json.
- Email with optional CSV attachment is sent if configured in config.json.

## Project Structure

- main.py: Main script to execute database query, save to CSV, and send email.

##### modules/: Directory containing all the module scripts.

- app.py: Class-based implementation encapsulating database queries, Excel saving, email sending, and file cleanup.
- config_loader.py: Class to load configuration from config.json.
- database_handler.py: Class to handle database connections and queries.
- email_sender.py: Class to handle email sending.
- excel_saver.py: Class to save query results to an Excel file.
- file_cleaner.py: Class to clean up old files in a directory.
- log.py: Logging setup and utility functions.