import allure
import pytest

from src.clients.orders_client import OrdersClient
from src.helpers.order_payloads import base_order_payload

@allure.feature("Orders")
@allure.story("Create order")
class TestOrdersCreate:

    @pytest.mark.parametrize(
        "colors",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
            None,
        ],
    )
    def test_create_order_returns_track(self, colors):
        client = OrdersClient()
        payload = base_order_payload(colors=colors)
        resp = client.create(payload)
        assert resp.status_code == 201
        body = resp.json()
        assert "track" in body and body["track"] is not None
