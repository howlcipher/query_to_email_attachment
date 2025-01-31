import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from .log import log

class EmailSender:
    def __init__(self, config):
        self.config = config
        self.sender_email = self.config['email']['sender_email']
        self.recipient_email = self.config['email']['recipient_email']
        self.subject = self.config['email']['subject']
        self.body = self.config['email']['body']
        self.empty_attachment_body = self.config['email']['empty_attachment_body']
        self.attachment = self.config['email']['attachment']
        self.attachment_source = self.config['email']['attachment_source']
        self.smtp_server = self.config['email']['smtp_server']
        self.smtp_port = self.config['email']['smtp_port']
        self.smtp_timeout = int(self.config['email']['smtp_timeout'])
        self.smtp_auth_required = bool(int(self.config['email']['smtp_auth_required']))
        self.sender_password = self.config['email']['sender_password']

    def send_email(self, query_results):
        try:
            # Build the email body with row count information
            body = self.body
            for sheet_name, df in query_results.items():
                row_count = len(df) if not df.empty else 0  # Exclude header row
                body += f"{sheet_name}: {row_count}\n"
            
            # Add the message body if data exists
            if self.attachment and self.attachment_source:
                if self.check_if_data_exists(self.attachment_source):
                    message_body = MIMEText(body, 'plain')
                else:
                    message_body = MIMEText(self.empty_attachment_body, 'plain')
            else:
                message_body = MIMEText(body, 'plain')

            # Setup the MIME message
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = ", ".join(self.recipient_email)
            message['Subject'] = self.subject
            message.attach(message_body)

            # Attach file if needed
            if self.attachment and self.attachment_source:
                filename = self.attachment_source
                with open(filename, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={filename}')
                message.attach(part)

            # Create SMTP session
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=self.smtp_timeout) as session:
                if self.smtp_auth_required:
                    session.starttls()  # Enable security if authentication is required
                    session.login(self.sender_email, self.sender_password)  # Login if authentication is required
                session.sendmail(self.sender_email, self.recipient_email, message.as_string())

            log("Email sent successfully.")
        except Exception as e:
            log(f"Error sending email: {e}")

    def check_if_data_exists(self, filepath):
        # Check if the file exists without trying to decode it as a text file
        if os.path.exists(filepath):
            try:
                # For binary files like .xlsx, we just check if it exists and is accessible
                with open(filepath, "rb") as file:
                    file.read(10)  # Try reading a small chunk to confirm it's accessible
                return True
            except Exception as e:
                log(f"Error reading file {filepath}: {e}")
                return False
        else:
            log(f"File {filepath} does not exist.")
            return False
