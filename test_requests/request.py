import os
import requests
from dotenv import load_dotenv
load_dotenv()
class CompletionClient:
    def __init__(self, language: str, url: str=None):
        if not url:
            url_template = os.getenv("FLCC_URL_TEMPLATE")
            assert url_template is not None, "URL is not specified"
            self.url = url_template.format(language=language)
        else:
            self.url = url
    def complete(self, file: str, prefix: str=""):
        requests.get(url