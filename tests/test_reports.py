import unittest
from unittest.mock import patch
from servicepytan.reports import (
    get_report_categories,
    get_report_list,
    get_dynamic_set_list,
    Report,
)


class TestReportsFunctions(unittest.TestCase):
    def setUp(self):
        self.conn = {"config": "data"}

    @patch("servicepytan.reports.endpoint_url")
    @patch("servicepytan.reports.request_json")
    def test_get_report_categories(self, mock_request_json, mock_endpoint_url):
        mock_endpoint_url.return_value = "http://fake.url/categories"
        mock_request_json.return_value = {"data": ["cat1"]}

        result = get_report_categories(conn=self.conn)

        mock_endpoint_url.assert_called_once_with(
            "reporting", "report-categories", conn=self.conn
        )
        mock_request_json.assert_called_once_with(
            "http://fake.url/categories", conn=self.conn
        )
        self.assertEqual(result, {"data": ["cat1"]})

    @patch("servicepytan.reports.endpoint_url")
    @patch("servicepytan.reports.request_json")
    def test_get_report_list(self, mock_request_json, mock_endpoint_url):
        mock_endpoint_url.return_value = "http://fake.url/list"
        mock_request_json.return_value = {"data": ["report1"]}

        result = get_report_list("jobs", conn=self.conn)

        mock_endpoint_url.assert_called_once_with(
            "reporting", "report-category/jobs/reports", conn=self.conn
        )
        mock_request_json.assert_called_once_with(
            "http://fake.url/list", conn=self.conn
        )
        self.assertEqual(result, {"data": ["report1"]})

    @patch("servicepytan.reports.endpoint_url")
    @patch("servicepytan.reports.request_json")
    def test_get_dynamic_set_list(self, mock_request_json, mock_endpoint_url):
        mock_endpoint_url.return_value = "http://fake.url/dynamic"
        mock_request_json.return_value = {"data": ["value1"]}

        result = get_dynamic_set_list("employees", conn=self.conn)

        mock_endpoint_url.assert_called_once_with(
            "reporting", "dynamic-value-sets/employees", conn=self.conn
        )
        mock_request_json.assert_called_once_with(
            "http://fake.url/dynamic", conn=self.conn
        )
        self.assertEqual(result, {"data": ["value1"]})


class TestReportClass(unittest.TestCase):
    def setUp(self):
        self.conn = {"config": "data"}
        with patch.object(
            Report, "get_metadata", return_value={"parameters": []}
        ) as mock_get_metadata:
            self.report = Report("jobs", "report1", conn=self.conn)
            self.mock_get_metadata = mock_get_metadata

    def test_init(self):
        self.assertEqual(self.report.category, "jobs")
        self.assertEqual(self.report.report_id, "report1")
        self.assertEqual(self.report.conn, self.conn)
        self.assertEqual(self.report.params, {"parameters": []})
        self.mock_get_metadata.assert_called_once()

    def test_add_and_get_params(self):
        self.report.add_params("StartDate", "2024-01-01")
        self.report.add_params("EndDate", "2024-01-31")

        params = self.report.get_params()
        self.assertEqual(
            params,
            {
                "parameters": [
                    {"name": "StartDate", "value": "2024-01-01"},
                    {"name": "EndDate", "value": "2024-01-31"},
                ]
            },
        )

    def test_update_params(self):
        self.report.add_params("StartDate", "2024-01-01")
        self.report.update_params("StartDate", "2024-02-01")

        params = self.report.get_params()
        self.assertEqual(params["parameters"][0]["value"], "2024-02-01")
        self.report.update_params("NewParam", "new_value")
        self.assertEqual(len(params["parameters"]), 2)
        self.assertEqual(params["parameters"][1]["name"], "NewParam")

    @patch("servicepytan.reports.endpoint_url")
    @patch("servicepytan.reports.request_json_with_retry")
    def test_get_metadata(self, mock_request_json, mock_endpoint_url):
        with patch.object(Report, "__init__", lambda s, c, r, co: None):
            report = Report(None, None, None)
            report.category = "jobs"
            report.report_id = "report1"
            report.conn = self.conn

        mock_endpoint_url.return_value = "http://fake.url/metadata"
        mock_request_json.return_value = {"metadata": "info"}

        result = report.get_metadata()

        mock_endpoint_url.assert_called_once_with(
            "reporting", "report-category/jobs/reports/report1", conn=self.conn
        )
        mock_request_json.assert_called_once_with(
            "http://fake.url/metadata", conn=self.conn
        )
        self.assertEqual(result, {"metadata": "info"})

    @patch("logging.Logger.info")
    def test_show_param_types(self, mock_log_info):
        self.report.metadata = {
            "parameters": [
                {
                    "name": "StartDate",
                    "dataType": "DateTime",
                    "isRequired": True,
                    "acceptValues": None,
                },
                {
                    "name": "BusinessUnit",
                    "dataType": "Long",
                    "isRequired": False,
                    "acceptValues": {
                        "dynamicSetId": "123",
                        "values": ["BU1", "BU2"],
                    },
                },
            ]
        }

        self.report.show_param_types()

        self.assertEqual(mock_log_info.call_count, 4)
        mock_log_info.assert_any_call("[*] - StartDate: DateTime, ")
        mock_log_info.assert_any_call(
            "[ ] - BusinessUnit: Long,  (dynamicSetId: 123)"
        )
        mock_log_info.assert_any_call("  - BU1")
        mock_log_info.assert_any_call("  - BU2")

    @patch("servicepytan.reports.endpoint_url")
    @patch("servicepytan.reports.request_json_with_retry")
    def test_get_data(self, mock_request_json, mock_endpoint_url):
        mock_endpoint_url.return_value = "http://fake.url/data"
        mock_request_json.return_value = {"data": "page_data"}

        result = self.report.get_data(params={"p": 1}, page=2, page_size=100)

        mock_endpoint_url.assert_called_once_with(
            "reporting",
            "report-category/jobs/reports/report1/data",
            conn=self.conn,
        )
        mock_request_json.assert_called_once_with(
            "http://fake.url/data",
            options={"page": 2, "pageSize": 100, "includeTotal": True},
            json_payload={"p": 1},
            conn=self.conn,
            request_type="POST",
        )
        self.assertEqual(result, {"data": "page_data"})

    @patch.object(Report, "get_data")
    def test_get_all_data(self, mock_get_data):
        mock_get_data.side_effect = [
            {"data": [1], "fields": ["f1"], "totalCount": 2, "hasMore": True},
            {"data": [2], "fields": ["f1"], "totalCount": 2, "hasMore": False},
        ]

        result = self.report.get_all_data()

        self.assertEqual(mock_get_data.call_count, 2)
        mock_get_data.assert_any_call(
            self.report.params, page=1, page_size=5000
        )
        mock_get_data.assert_any_call(
            self.report.params, page=2, page_size=5000
        )
        self.assertEqual(result, {"data": [1, 2], "fields": ["f1"]})

    @patch.object(Report, "get_data")
    @patch("logging.Logger.warning")
    def test_get_all_data_timeout(self, mock_log_warning, mock_get_data):
        mock_get_data.return_value = {
            "data": [1],
            "fields": ["f1"],
            "totalCount": 1000000,
            "hasMore": True,
        }

        result = self.report.get_all_data(timeout_min=10)

        mock_get_data.assert_called_once()
        mock_log_warning.assert_called()
        self.assertEqual(
            result,
            {"error": "Too many requests. Try again with fewer parameters."},
        )


if __name__ == "__main__":
    unittest.main()
