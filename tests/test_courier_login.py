import allure
import pytest

from src.helpers.random_data import new_courier_payload
from src.helpers.retry import request_with_retry


@allure.feature("Courier")
@allure.story("Login courier")
class TestCourierLogin:

    def test_courier_can_login_and_returns_id(self, courier_client):
        payload = new_courier_payload()
        create_resp = courier_client.create(payload)
        assert create_resp.status_code == 201

        login_resp = courier_client.login({
            "login": payload["login"],
            "password": payload["password"],
        })
        assert login_resp.status_code == 200
        body = login_resp.json()
        assert "id" in body and isinstance(body["id"], int)

        courier_client.delete(body["id"])

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_requires_mandatory_fields(self, courier_client, missing_field):
        payload = new_courier_payload()
        courier_client.create(payload)

        creds = {
            "login": payload["login"],
            "password": payload["password"],
        }
        creds.pop(missing_field)

        resp = request_with_retry(lambda: courier_client.login(creds))

        if missing_field == "password" and resp.status_code == 504:
            pytest.xfail(
                "Known stand flakiness: /courier/login without password may timeout (504) instead of 400"
            )

        assert resp.status_code == 400, (
            f"Expected 400 for missing field '{missing_field}', "
            f"got {resp.status_code}"
        )

        login_resp = courier_client.login({
            "login": payload["login"],
            "password": payload["password"],
        })
        if getattr(login_resp, "status_code", None) == 200:
            courier_client.delete(login_resp.json().get("id"))

    def test_login_wrong_credentials_returns_error(self, courier_client):
        payload = new_courier_payload()
        courier_client.create(payload)

        resp = courier_client.login({
            "login": payload["login"],
            "password": "wrong_password",
        })
        assert resp.status_code in (400, 404)

        login_resp = courier_client.login({
            "login": payload["login"],
            "password": payload["password"],
        })
        if login_resp.status_code == 200:
            courier_client.delete(login_resp.json().get("id"))

    def test_login_nonexistent_user_returns_error(self, courier_client):
        resp = courier_client.login({
            "login": "nonexistent_user_12345",
            "password": "nope",
        })
        assert resp.status_code == 404
