from abc import ABC, abstractmethod
from typing import List, Dict
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class WebScraper(ABC):
    @abstractmethod
    def scrape(self, url: str) -> List[Dict[str, str]]:
        pass

class NavigationScraper(WebScraper):
    def __init__(self):
        self.logger = logging.getLogger(__name__ + ".NavigationScraper")

    @staticmethod
    def get_domain(url: str) -> str:
        return urlparse(url).netloc

    def scrape(self, url: str) -> List[Dict[str, str]]:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            self.logger.info(f"Scraping navigation links from {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            nav_elements = soup.find_all('nav') or soup.find_all(['ul', 'div'], 
                                                                class_=['menu', 'navigation', 'nav', 'navbar'])
            
            domain = self.get_domain(url)
            nav_links = []
            
            for nav in nav_elements:
                for link in nav.find_all('a'):
                    href = link.get('href')
                    if href:
                        full_url = urljoin(url, href)
                        if self.get_domain(full_url) == domain:
                            nav_links.append({
                                'text': link.text.strip(),
                                'url': full_url
                            })
            
            self.logger.info(f"Found {len(nav_links)} navigation links")
            return nav_links
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {str(e)}")
            return []