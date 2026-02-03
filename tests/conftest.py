import pytest
import allure

from src.clients.courier_client import CourierClient
from src.helpers.random_data import new_courier_payload

@pytest.fixture()
def courier_client():
    return CourierClient()

@pytest.fixture()
def created_courier(courier_client):
    """Создаёт курьера и удаляет его в teardown (если удалось залогиниться)."""
    payload = new_courier_payload()
    with allure.step("Create courier"):
        create_resp = courier_client.create(payload)

    courier_id = None
    if create_resp.status_code in (201, 409):
        with allure.step("Login courier to get id"):
            login_resp = courier_client.login({"login": payload["login"], "password": payload["password"]})
        if login_resp.status_code == 200:
            body = login_resp.json()
            courier_id = body.get("id")

    yield payload, create_resp, courier_id

    if courier_id is not None:
        with allure.step("Delete courier"):
            courier_client.delete(courier_id)
