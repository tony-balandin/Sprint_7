from typing import Dict, Any, Optional
from src.clients.base_client import BaseClient
from src.config import API_V1

class OrdersClient(BaseClient):
    ORDERS_PATH = f"{API_V1}/orders"

    def create(self, payload: Dict[str, Any]):
        return self.session.post(self.url(self.ORDERS_PATH), json=payload)

    def list(self, params: Optional[Dict[str, Any]] = None):
        return self.session.get(self.url(self.ORDERS_PATH), params=params)
