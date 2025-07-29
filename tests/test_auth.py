import unittest
from unittest.mock import patch, mock_open
import os
import requests_mock
from servicepytan.auth import (
    ApiEnvironment,
    get_auth_root_url,
    get_api_root_url,
    servicepytan_connect,
    request_auth_token,
    get_auth_token,
    get_app_key,
    get_tenant_id,
    get_auth_headers,
)


class TestAuth(unittest.TestCase):

    def test_get_auth_root_url(self):
        self.assertEqual(
            get_auth_root_url(ApiEnvironment.PRODUCTION),
            "https://auth.servicetitan.io",
        )
        self.assertEqual(
            get_auth_root_url(ApiEnvironment.INTEGRATION),
            "https://auth-integration.servicetitan.io",
        )
        with self.assertRaises(ValueError):
            get_auth_root_url("unknown_env")

    def test_get_api_root_url(self):
        self.assertEqual(
            get_api_root_url(ApiEnvironment.PRODUCTION),
            "https://api.servicetitan.io",
        )
        self.assertEqual(
            get_api_root_url(ApiEnvironment.INTEGRATION),
            "https://api-integration.servicetitan.io",
        )
        with self.assertRaises(ValueError):
            get_api_root_url("unknown_env")

    def test_servicepytan_connect_with_params(self):
        conn = servicepytan_connect(
            api_environment=ApiEnvironment.PRODUCTION,
            app_key="test_app_key",
            tenant_id="test_tenant_id",
            client_id="test_client_id",
            client_secret="test_client_secret",
        )
        self.assertEqual(conn["SERVICETITAN_APP_KEY"], "test_app_key")
        self.assertEqual(conn["SERVICETITAN_TENANT_ID"], "test_tenant_id")
        self.assertEqual(conn["SERVICETITAN_CLIENT_ID"], "test_client_id")
        self.assertEqual(
            conn["SERVICETITAN_CLIENT_SECRET"], "test_client_secret"
        )
        self.assertEqual(conn["api_root"], "https://api.servicetitan.io")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"SERVICETITAN_APP_KEY": "file_app_key", "SERVICETITAN_TENANT_ID": "file_tenant_id", "SERVICETITAN_CLIENT_ID": "file_client_id", "SERVICETITAN_CLIENT_SECRET": "file_client_secret"}',
    )
    def test_servicepytan_connect_with_config_file(self, mock_file):
        conn = servicepytan_connect(config_file="dummy/path.json")
        mock_file.assert_called_with("dummy/path.json")
        self.assertEqual(conn["SERVICETITAN_APP_KEY"], "file_app_key")
        self.assertEqual(conn["SERVICETITAN_TENANT_ID"], "file_tenant_id")

    @patch.dict(
        os.environ,
        {
            "SERVICETITAN_APP_KEY": "env_app_key",
            "SERVICETITAN_TENANT_ID": "env_tenant_id",
            "SERVICETITAN_CLIENT_ID": "env_client_id",
            "SERVICETITAN_CLIENT_SECRET": "env_client_secret",
        },
    )
    def test_servicepytan_connect_with_env_vars(self):
        conn = servicepytan_connect()
        self.assertEqual(conn["SERVICETITAN_APP_KEY"], "env_app_key")
        self.assertEqual(conn["SERVICETITAN_TENANT_ID"], "env_tenant_id")

    @requests_mock.Mocker()
    def test_request_auth_token(self, m):
        auth_url = "https://auth.servicetitan.io/connect/token"
        m.post(
            auth_url, json={"access_token": "test_token", "expires_in": 3600}
        )

        token_data = request_auth_token(
            "https://auth.servicetitan.io", "client_id", "client_secret"
        )
        self.assertEqual(token_data["access_token"], "test_token")

    @patch("servicepytan.auth.request_auth_token")
    def test_get_auth_token(self, mock_request_auth_token):
        mock_request_auth_token.return_value = {"access_token": "mocked_token"}
        conn = {
            "SERVICETITAN_CLIENT_ID": "client_id",
            "SERVICETITAN_CLIENT_SECRET": "client_secret",
            "auth_root": "https://auth.servicetitan.io",
        }
        token = get_auth_token(conn)
        self.assertEqual(token, "mocked_token")
        mock_request_auth_token.assert_called_with(
            "https://auth.servicetitan.io", "client_id", "client_secret"
        )

    def test_get_app_key(self):
        conn = {"SERVICETITAN_APP_KEY": "my_app_key"}
        self.assertEqual(get_app_key(conn), "my_app_key")

    def test_get_tenant_id(self):
        conn = {"SERVICETITAN_TENANT_ID": "my_tenant_id"}
        self.assertEqual(get_tenant_id(conn), "my_tenant_id")

    @patch("servicepytan.auth.get_auth_token")
    def test_get_auth_headers(self, mock_get_auth_token):
        mock_get_auth_token.return_value = "mocked_token"
        conn = {"SERVICETITAN_APP_KEY": "my_app_key"}
        headers = get_auth_headers(conn)
        self.assertEqual(
            headers,
            {
                "Authorization": "Bearer mocked_token",
                "ST-App-Key": "my_app_key",
            },
        )
        mock_get_auth_token.assert_called_with(conn)


if __name__ == "__main__":
    unittest.main()
