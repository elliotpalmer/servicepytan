import unittest
from unittest.mock import patch, mock_open
from servicepytan.requests import Endpoint


class TestRequests(unittest.TestCase):

    def setUp(self):
        self.conn = {"config": "data"}
        self.endpoint = Endpoint("jpm", "jobs", conn=self.conn)

    @patch(
        "servicepytan.requests.check_default_options", side_effect=lambda x: x
    )
    @patch("servicepytan.requests.endpoint_url")
    @patch("servicepytan.requests.request_json")
    def test_get_one(
        self, mock_request_json, mock_endpoint_url, mock_check_options
    ):
        mock_endpoint_url.return_value = "http://fake.url/one"
        mock_request_json.return_value = {"id": 1, "name": "Job 1"}

        result = self.endpoint.get_one(
            id="123", modifier="notes", query={"param": "value"}
        )

        mock_endpoint_url.assert_called_once_with(
            "jpm", "jobs", id="123", modifier="notes", conn=self.conn
        )
        mock_check_options.assert_called_once_with({"param": "value"})
        mock_request_json.assert_called_once_with(
            "http://fake.url/one",
            options={"param": "value"},
            payload="",
            conn=self.conn,
            request_type="GET",
        )
        self.assertEqual(result, {"id": 1, "name": "Job 1"})

    @patch(
        "servicepytan.requests.check_default_options", side_effect=lambda x: x
    )
    @patch("servicepytan.requests.endpoint_url")
    @patch("servicepytan.requests.request_json")
    def test_get_many(
        self, mock_request_json, mock_endpoint_url, mock_check_options
    ):
        mock_endpoint_url.return_value = "http://fake.url/many"
        mock_request_json.return_value = {
            "data": [{"id": 1}],
            "hasMore": False,
        }

        result = self.endpoint.get_many(query={"pageSize": 10})

        mock_endpoint_url.assert_called_once_with(
            "jpm", "jobs", id="", modifier="", conn=self.conn
        )
        mock_check_options.assert_called_once_with({"pageSize": 10})
        mock_request_json.assert_called_once_with(
            "http://fake.url/many",
            {"pageSize": 10},
            payload="",
            conn=self.conn,
            request_type="GET",
        )
        self.assertEqual(result, {"data": [{"id": 1}], "hasMore": False})

    @patch.object(Endpoint, "get_many")
    def test_get_all(self, mock_get_many):
        mock_get_many.side_effect = [
            {"data": [{"id": 1}], "hasMore": True},
            {"data": [{"id": 2}], "hasMore": False},
        ]

        result = self.endpoint.get_all(query={"status": "Completed"})

        self.assertEqual(mock_get_many.call_count, 2)
        mock_get_many.assert_any_call(
            query={"status": "Completed", "page": "1"}, id="", modifier=""
        )
        mock_get_many.assert_any_call(
            query={"status": "Completed", "page": "2"}, id="", modifier=""
        )
        self.assertEqual(result, [{"id": 1}, {"id": 2}])

    @patch("servicepytan.requests.endpoint_url")
    @patch("servicepytan.requests.request_json")
    def test_create(self, mock_request_json, mock_endpoint_url):
        mock_endpoint_url.return_value = "http://fake.url/create"
        mock_request_json.return_value = {"id": 3, "status": "new"}
        payload = {"name": "New Job"}

        result = self.endpoint.create(payload)

        mock_endpoint_url.assert_called_once_with(
            "jpm", "jobs", conn=self.conn
        )
        mock_request_json.assert_called_once_with(
            "http://fake.url/create",
            options={},
            json_payload=payload,
            conn=self.conn,
            request_type="POST",
        )
        self.assertEqual(result, {"id": 3, "status": "new"})

    @patch("servicepytan.requests.endpoint_url")
    @patch("servicepytan.requests.request_json")
    def test_update(self, mock_request_json, mock_endpoint_url):
        mock_endpoint_url.return_value = "http://fake.url/update"
        mock_request_json.return_value = {"id": 1, "status": "updated"}
        payload = {"name": "Updated Job"}

        result = self.endpoint.update("123", payload, request_type="PATCH")

        mock_endpoint_url.assert_called_once_with(
            "jpm", "jobs", id="123", modifier="", conn=self.conn
        )
        mock_request_json.assert_called_once_with(
            "http://fake.url/update",
            options={},
            payload=payload,
            conn=self.conn,
            request_type="PATCH",
        )
        self.assertEqual(result, {"id": 1, "status": "updated"})

    @patch("servicepytan.requests.endpoint_url")
    @patch("servicepytan.requests.request_json")
    def test_delete(self, mock_request_json, mock_endpoint_url):
        mock_endpoint_url.return_value = "http://fake.url/delete"
        mock_request_json.return_value = {"status": "deleted"}

        result = self.endpoint.delete("123")

        mock_endpoint_url.assert_called_once_with(
            "jpm", "jobs", id="123", modifier="", conn=self.conn
        )
        mock_request_json.assert_called_once_with(
            "http://fake.url/delete",
            options={},
            payload="",
            conn=self.conn,
            request_type="DEL",
        )
        self.assertEqual(result, {"status": "deleted"})

    @patch("servicepytan.requests.endpoint_url")
    @patch("servicepytan.requests.request_json")
    def test_delete_subitem(self, mock_request_json, mock_endpoint_url):
        mock_endpoint_url.return_value = "http://fake.url/delete_sub"
        mock_request_json.return_value = {"status": "subitem_deleted"}

        result = self.endpoint.delete_subitem("123", "note_456", "notes")

        mock_endpoint_url.assert_called_once_with(
            "jpm", "jobs", id="123", modifier="notes/note_456", conn=self.conn
        )
        mock_request_json.assert_called_once_with(
            "http://fake.url/delete_sub",
            options={},
            payload="",
            conn=self.conn,
            request_type="DEL",
        )
        self.assertEqual(result, {"status": "subitem_deleted"})

    @patch("servicepytan.requests.endpoint_url")
    @patch("servicepytan.requests.request_json")
    def test_export_one(self, mock_request_json, mock_endpoint_url):
        export_endpoint = Endpoint("jpm", "export", conn=self.conn)
        mock_endpoint_url.return_value = "http://fake.url/export_one"
        mock_request_json.return_value = {
            "data": [{"id": 1}],
            "hasMore": True,
            "continueFrom": "token1",
        }

        result = export_endpoint.export_one(
            "jobs_export",
            export_from="start_token",
            include_recent_changes=True,
        )

        mock_endpoint_url.assert_called_once_with(
            "jpm", "export", id="", modifier="jobs_export", conn=self.conn
        )
        mock_request_json.assert_called_once_with(
            "http://fake.url/export_one",
            options={"from": "start_token", "includeRecentChanges": True},
            payload="",
            conn=self.conn,
            request_type="GET",
        )
        self.assertEqual(
            result,
            {"data": [{"id": 1}], "hasMore": True, "continueFrom": "token1"},
        )

    @patch.object(Endpoint, "export_one")
    def test_export_all(self, mock_export_one):
        export_endpoint = Endpoint("jpm", "export", conn=self.conn)
        mock_export_one.side_effect = [
            {"data": [{"id": 1}], "hasMore": True, "continueFrom": "token1"},
            {"data": [{"id": 2}], "hasMore": False, "continueFrom": None},
        ]

        result = export_endpoint.export_all("jobs_export")

        self.assertEqual(mock_export_one.call_count, 2)
        mock_export_one.assert_any_call("jobs_export", "", False)
        mock_export_one.assert_any_call("jobs_export", "token1", False)
        self.assertEqual(result, [{"id": 1}, {"id": 2}])

    @patch("servicepytan.requests.endpoint_url")
    @patch("servicepytan.requests.request_contents")
    @patch("builtins.open", new_callable=mock_open)
    def test_download(
        self, mock_file, mock_request_contents, mock_endpoint_url
    ):
        download_endpoint = Endpoint(
            "forms", "jobs/attachment", conn=self.conn
        )

        mock_endpoint_url.return_value = "http://fake.url/download"
        mock_request_contents.return_value = b"file data"

        result = download_endpoint.download("123", filename="test.txt")

        mock_endpoint_url.assert_called_once_with(
            "forms", "jobs/attachment", id="123", modifier="", conn=self.conn
        )
        mock_request_contents.assert_called_once_with(
            "http://fake.url/download", options={}, conn=self.conn
        )
        mock_file.assert_called_once_with("test.txt", "wb")
        mock_file().write.assert_called_once_with(b"file data")
        self.assertEqual(result, b"file data")

    def test_download_invalid_endpoint(self):
        with self.assertRaisesRegex(
            ValueError, "Download method is not supported for endpoint 'jobs'"
        ):
            self.endpoint.download("123")

    def test_download_no_id(self):
        download_endpoint = Endpoint("forms", "attachments", conn=self.conn)
        with self.assertRaisesRegex(
            ValueError, "ID must be provided to download a file."
        ):
            download_endpoint.download("")


if __name__ == "__main__":
    unittest.main()
