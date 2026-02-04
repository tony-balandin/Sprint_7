import allure

from src.helpers.retry import request_with_retry


@allure.feature("Courier")
@allure.story("Login courier")
class TestCourierLogin:

    def test_login_returns_200(self, courier_client, registered_courier):
        resp = courier_client.login({
            "login": registered_courier["login"],
            "password": registered_courier["password"],
        })
        assert resp.status_code == 200

    def test_login_returns_id(self, courier_client, registered_courier):
        resp = courier_client.login({
            "login": registered_courier["login"],
            "password": registered_courier["password"],
        })
        assert "id" in resp.json()

    def test_login_wrong_credentials_returns_error(self, courier_client, registered_courier):
        resp = courier_client.login({
            "login": registered_courier["login"],
            "password": "wrong_password",
        })
        assert resp.status_code in (400, 404)

    def test_login_without_login_returns_error(self, courier_client, registered_courier):
        resp = courier_client.login({
            "password": registered_courier["password"],
        })
        assert resp.status_code == 400

    def test_login_without_password_returns_error(self, courier_client, registered_courier):
        resp = request_with_retry(lambda: courier_client.login({
            "login": registered_courier["login"],
            "password": "",
        }))
        assert resp.status_code == 400

    def test_login_nonexistent_user_returns_error(self, courier_client):
        resp = courier_client.login({"login": "nonexistent_user_12345", "password": "nope"})
        assert resp.status_code == 404
