import pytest

from src.clients.courier_client import CourierClient
from src.helpers.random_data import new_courier_payload
from src.helpers.retry import request_with_retry


@pytest.fixture()
def courier_client():
    return CourierClient()


@pytest.fixture()
def courier_payload():
    return new_courier_payload()


@pytest.fixture()
def courier_cleanup(courier_client):
    """Post-conditions: delete couriers created during a test."""
    creds_list = []

    def register(creds: dict):
        creds_list.append(creds)

    yield register

    for creds in creds_list:
        try:
            login_resp = request_with_retry(
                lambda: courier_client.login({"login": creds.get("login"), "password": creds.get("password")})
            )
            if getattr(login_resp, "status_code", None) == 200:
                courier_id = login_resp.json().get("id")
                if courier_id:
                    courier_client.delete(courier_id)
        except Exception:
            pass


@pytest.fixture()
def registered_courier(courier_client, courier_payload, courier_cleanup):
    """Precondition courier for login tests (registration itself is not under test here)."""
    courier_client.create(courier_payload)
    courier_cleanup(courier_payload)
    return courier_payload
