import requests
from typing import Any, Optional, Type

from bs4 import BeautifulSoup


class BS4ScrapperAdapter:
    def __init__(
        self,
        url: Optional[str] = None,
        html_body: Optional[str] = None,
        scrapper_client: Type[BeautifulSoup] = BeautifulSoup,
        http_client: Optional[Any] = requests,
    ):
        self.url = url
        self.html_body = html_body
        self.scrapper_client = scrapper_client
        self.http_client = http_client
        self.http_request = None
        self.http_response = None
        self.scrapper = scrapper_client(
            self.html_body, features="html.parser"
        ) if html_body else None

    def get_html(self):
        response = self.http_client.get(self.url)
        self.http_request = response.request
        self.http_response = response
        if response.status_code == 200:
            self.html_body = response.text
            self.scrapper = self.scrapper_client(self.html_body, features="html.parser")
            return self.html_body

    def get_text_by_span_id(self, span_id: str) -> Optional[str]:
        response = self.scrapper.find("span", id=span_id)
        return response.text if response else None
