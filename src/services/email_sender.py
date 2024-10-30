from abc import ABC, abstractmethod
import logging
from typing import Tuple
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> Tuple[bool, str]:
        pass

class GmailSender(EmailSender):
    def __init__(self, sender_email: str, sender_password: str):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.logger = logging.getLogger(__name__ + ".GmailSender")

    def send(self, to: str, subject: str, body: str) -> Tuple[bool, str]:
        try:
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = to
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            
            self.logger.info(f"Attempting to send email to {to}")
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to, message.as_string())
            
            self.logger.info(f"Successfully sent email to {to}")
            return True, "Email sent successfully"
        except Exception as e:
            self.logger.error(f"Failed to send email to {to}: {str(e)}")
            return False, f"Failed to send email: {str(e)}"