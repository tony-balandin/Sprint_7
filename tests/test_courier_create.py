import allure
import pytest

from src.helpers.random_data import new_courier_payload


@allure.feature("Courier")
@allure.story("Create courier")
class TestCourierCreate:

    def test_create_returns_201(self, courier_client, courier_cleanup):
        payload = new_courier_payload()
        resp = courier_client.create(payload)
        courier_cleanup(payload)

        assert resp.status_code == 201

    def test_create_returns_ok_true(self, courier_client, courier_cleanup):
        payload = new_courier_payload()
        resp = courier_client.create(payload)
        courier_cleanup(payload)

        assert resp.json() == {"ok": True}

    def test_cannot_create_duplicate_courier(self, courier_client, courier_cleanup):
        payload = new_courier_payload()
        courier_client.create(payload)
        courier_cleanup(payload)

        resp = courier_client.create(payload)
        assert resp.status_code == 409

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_requires_login_and_password(self, courier_client, missing_field):
        payload = new_courier_payload()
        payload.pop(missing_field)

        resp = courier_client.create(payload)
        assert resp.status_code == 400

    def test_create_existing_login_returns_error(self, courier_client, courier_cleanup):
        payload1 = new_courier_payload()
        courier_client.create(payload1)
        courier_cleanup(payload1)

        payload2 = new_courier_payload()
        payload2["login"] = payload1["login"]

        resp = courier_client.create(payload2)
        assert resp.status_code == 409
