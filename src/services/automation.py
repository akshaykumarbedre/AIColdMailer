import os
import csv
import logging
from dataclasses import asdict
from typing import List
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.models.schemas import Target, EmailContent
from src.llm.options import LLMOption
from src.services.scraper import NavigationScraper
from src.services.email_generator import LangChainEmailGenerator
from src.services.email_sender import GmailSender
from src.config import Config

class ColdEmailAutomation:
    def __init__(self, config: Config):
        self.config = config
        self.scraper = NavigationScraper()
        self.email_sender = GmailSender(config.SENDER_EMAIL, config.SENDER_PASSWORD)
        self.csv_file = os.path.join("data", "generated_emails.csv")
        self._ensure_data_directory()
        self.logger = logging.getLogger(__name__ + ".ColdEmailAutomation")

    def _ensure_data_directory(self):
        os.makedirs("data", exist_ok=True)

    def process_target(self, target: Target, purpose: str, prompt: str,
                      llm_option: LLMOption) -> EmailContent:
        try:
            self.email_generator = LangChainEmailGenerator(llm_option)
            nav_links = self.scraper.scrape(target.website)
            web_urls = {link['url'] for link in nav_links}
            web_urls.add(target.website)
            
            web_urls = sorted(list(web_urls), key=len)[:2]  # Limit to 2 pages for efficiency
            
            doc = WebBaseLoader(web_path=web_urls).load()
            chunk_doc = RecursiveCharacterTextSplitter(
                chunk_size=5000, 
                chunk_overlap=100
            ).split_documents(doc)

            email_result = self.email_generator.generate(chunk_doc, purpose, prompt)
            
            return EmailContent(
                website=target.website,
                email=target.email,
                subject=email_result["subject"],
                body=email_result["body"]
            )
        except Exception as e:
            self.logger.error(f"Error processing target {target.website}: {str(e)}")
            return EmailContent(
                website=target.website,
                email=target.email,
                subject="Error",
                body=f"Failed to generate email: {str(e)}",
                status="Failed"
            )

    def save_to_csv(self, email_content: EmailContent):
        file_exists = os.path.isfile(self.csv_file)
        with open(self.csv_file, mode='a', newline='', encoding='utf-8') as file:
            fieldnames = ['website', 'email', 'subject', 'body', 'status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(asdict(email_content))

    def update_csv_status(self, email: str, new_status: str):
        temp_file = os.path.join("data", "temp_emails.csv")
        with open(self.csv_file, mode='r', newline='', encoding='utf-8') as infile, \
             open(temp_file, mode='w', newline='', encoding='utf-8') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                if row['email'] == email:
                    row['status'] = new_status
                writer.writerow(row)
        os.replace(temp_file, self.csv_file)

    def send_email(self, email_content: EmailContent) -> bool:
        success, _ = self.email_sender.send(
            email_content.email,
            email_content.subject,
            email_content.body
        )
        if success:
            self.update_csv_status(email_content.email, "Sent")
        return success