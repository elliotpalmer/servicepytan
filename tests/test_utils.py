import unittest
from unittest.mock import patch, mock_open
import requests_mock
from servicepytan.utils import (
    request_json,
    check_default_options,
    endpoint_url,
    create_credential_file,
    get_timezone_by_file,
    sleep_with_countdown,
    request_json_with_retry,
    request_contents,
)


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.conn = {
            "SERVICETITAN_TENANT_ID": "12345",
            "api_root": "https://api.servicetitan.io",
            "SERVICETITAN_TIMEZONE": "America/New_York",
            "SERVICETITAN_APP_KEY": "some_app_key",
            "SERVICETITAN_CLIENT_ID": "some_client_id",
            "SERVICETITAN_CLIENT_SECRET": "some_client_secret",
            "auth_root": "https://auth.servicetitan.io",
        }

    @patch("servicepytan.utils.get_auth_headers")
    @requests_mock.Mocker()
    def test_request_json(self, mock_auth_headers, m):
        mock_auth_headers.return_value = {
            "Authorization": "Bearer token",
            "ST-App-Key": "key",
        }
        m.get("https://api.servicetitan.io/test", json={"data": "success"})

        response = request_json(
            "https://api.servicetitan.io/test", conn=self.conn
        )
        self.assertEqual(response, {"data": "success"})

    def test_check_default_options(self):
        options = {}
        self.assertEqual(check_default_options(options), {"pageSize": 100})
        options = {"pageSize": 50}
        self.assertEqual(check_default_options(options), {"pageSize": 50})

    def test_endpoint_url(self):
        url = endpoint_url("jpm", "jobs", conn=self.conn)
        self.assertEqual(
            url, "https://api.servicetitan.io/jpm/v2/tenant/12345/jobs"
        )

        url = endpoint_url("jpm", "jobs", id="67890", conn=self.conn)
        self.assertEqual(
            url, "https://api.servicetitan.io/jpm/v2/tenant/12345/jobs/67890"
        )

        url = endpoint_url(
            "jpm", "jobs", id="67890", modifier="notes", conn=self.conn
        )
        self.assertEqual(
            url,
            "https://api.servicetitan.io/jpm/v2/tenant/12345/jobs/67890/notes",
        )

    @patch("builtins.open", new_callable=mock_open)
    def test_create_credential_file(self, mock_file):
        create_credential_file("test_config.json")
        mock_file.assert_called_with("test_config.json", "w")
        handle = mock_file()
        written_content = handle.write.call_args[0][0]
        import json

        data = json.loads(written_content)
        self.assertIn("SERVICETITAN_CLIENT_ID", data)

    def test_get_timezone_by_file(self):
        self.assertEqual(get_timezone_by_file(self.conn), "America/New_York")
        self.assertEqual(get_timezone_by_file({}), "UTC")
        self.assertEqual(get_timezone_by_file(None), "UTC")

    @patch("time.sleep")
    @patch("logging.Logger.info")
    def test_sleep_with_countdown(self, mock_log, mock_sleep):
        sleep_with_countdown(3)
        self.assertEqual(mock_sleep.call_count, 3)
        mock_sleep.assert_called_with(1)

    @patch("servicepytan.utils.request_json")
    @patch("servicepytan.utils.sleep_with_countdown")
    def test_request_json_with_retry(self, mock_sleep, mock_request_json):
        rate_limit_response = {
            "status": 429,
            "title": "Rate limit exceeded. Try again in 60 seconds.",
            "traceId": "some_trace_id",
        }
        success_response = {"data": "success"}

        mock_request_json.side_effect = [rate_limit_response, success_response]

        response = request_json_with_retry("http://test.com", conn=self.conn)

        self.assertEqual(mock_request_json.call_count, 2)
        mock_sleep.assert_called_once_with(60)
        self.assertEqual(response, success_response)

    @patch("servicepytan.utils.get_auth_headers")
    @requests_mock.Mocker()
    def test_request_contents(self, mock_auth_headers, m):
        mock_auth_headers.return_value = {
            "Authorization": "Bearer token",
            "ST-App-Key": "key",
        }
        m.get("https://api.servicetitan.io/test", content=b"file content")

        response = request_contents(
            "https://api.servicetitan.io/test", conn=self.conn
        )
        self.assertEqual(response, b"file content")


if __name__ == "__main__":
    unittest.main()
