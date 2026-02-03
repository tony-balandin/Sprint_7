import allure

from src.clients.orders_client import OrdersClient

@allure.feature("Orders")
@allure.story("List orders")
def test_orders_list_returns_orders_list():
    client = OrdersClient()
    resp = client.list()
    assert resp.status_code == 200
    body = resp.json()
    assert "orders" in body
    assert isinstance(body["orders"], list)
