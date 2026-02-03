from typing import Dict, Any
from src.clients.base_client import BaseClient
from src.config import API_V1

class CourierClient(BaseClient):
    COURIER_PATH = f"{API_V1}/courier"
    LOGIN_PATH = f"{API_V1}/courier/login"

    def create(self, payload: Dict[str, Any]):
        return self.session.post(self.url(self.COURIER_PATH), data=payload)

    def login(self, payload: Dict[str, Any]):
        return self.session.post(
            self.url(self.LOGIN_PATH),
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=20,
        )

    def delete(self, courier_id: int):
        return self.session.delete(self.url(f"{self.COURIER_PATH}/{courier_id}"))
