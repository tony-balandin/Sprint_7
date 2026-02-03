import requests
from src.config import BASE_URL

class BaseClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def url(self, path: str) -> str:
        if path.startswith("http"):
            return path
        return f"{self.base_url}{path}"
