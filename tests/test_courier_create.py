import allure
import pytest

from src.helpers.random_data import new_courier_payload

@allure.feature("Courier")
@allure.story("Create courier")
class TestCourierCreate:

    def test_courier_can_be_created(self, courier_client, created_courier):
        _, create_resp, _ = created_courier
        assert create_resp.status_code == 201
        assert create_resp.json() == {"ok": True}

    def test_cannot_create_duplicate_courier(self, courier_client):
        payload = new_courier_payload()
        resp1 = courier_client.create(payload)
        assert resp1.status_code == 201

        resp2 = courier_client.create(payload)
        assert resp2.status_code == 409

        login = courier_client.login({"login": payload["login"], "password": payload["password"]})
        if login.status_code == 200:
            courier_id = login.json().get("id")
            if courier_id:
                courier_client.delete(courier_id)

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_requires_login_and_password(self, courier_client, missing_field):
        payload = new_courier_payload()
        payload.pop(missing_field)
        resp = courier_client.create(payload)
        assert resp.status_code == 400

    def test_create_existing_login_returns_error(self, courier_client):
        payload1 = new_courier_payload()
        resp1 = courier_client.create(payload1)
        assert resp1.status_code == 201

        payload2 = new_courier_payload()
        payload2["login"] = payload1["login"]
        resp2 = courier_client.create(payload2)
        assert resp2.status_code == 409

        login = courier_client.login({"login": payload1["login"], "password": payload1["password"]})
        if login.status_code == 200:
            courier_id = login.json().get("id")
            if courier_id:
                courier_client.delete(courier_id)
