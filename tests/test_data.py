import unittest
from unittest.mock import patch
from servicepytan.data import DataService


@patch(
    "servicepytan.data._convert_date_to_api_format", side_effect=lambda d, t: d
)
class TestDataService(unittest.TestCase):

    def setUp(self):
        self.conn = {"SERVICETITAN_TIMEZONE": "UTC"}

    @patch("servicepytan.data.Endpoint")
    def test_get_jobs_completed_between(self, MockEndpoint, mock_convert_date):
        mock_endpoint_instance = MockEndpoint.return_value
        mock_endpoint_instance.get_all.return_value = [{"id": 1}]

        data_service = DataService(conn=self.conn)
        result = data_service.get_jobs_completed_between(
            "start", "end", job_status=["Completed"]
        )

        MockEndpoint.assert_called_with("jpm", "jobs")
        mock_endpoint_instance.get_all.assert_called_once_with(
            {
                "jobStatus": "Completed",
                "completedOnOrAfter": "start",
                "completedBefore": "end",
            }
        )
        self.assertEqual(result, [{"id": 1}])

    @patch("servicepytan.data.Endpoint")
    def test_get_jobs_created_between(self, MockEndpoint, mock_convert_date):
        mock_endpoint_instance = MockEndpoint.return_value
        mock_endpoint_instance.get_all.return_value = [{"id": 2}]

        data_service = DataService(conn=self.conn)
        result = data_service.get_jobs_created_between("start", "end")

        MockEndpoint.assert_called_with("jpm", "jobs")
        mock_endpoint_instance.get_all.assert_called_once_with(
            {"createdOnOrAfter": "start", "createdBefore": "end"}
        )
        self.assertEqual(result, [{"id": 2}])

    @patch("servicepytan.data.Endpoint")
    def test_get_appointments_between(self, MockEndpoint, mock_convert_date):
        mock_endpoint_instance = MockEndpoint.return_value
        mock_endpoint_instance.get_all.return_value = [{"id": 3}]

        data_service = DataService(conn=self.conn)
        result = data_service.get_appointments_between(
            "start", "end", appointment_status=["Scheduled"]
        )

        MockEndpoint.assert_called_with("jpm", "appointments")
        mock_endpoint_instance.get_all.assert_called_once_with(
            {
                "status": "Scheduled",
                "startsOnOrAfter": "start",
                "startsBefore": "end",
            }
        )
        self.assertEqual(result, [{"id": 3}])

    @patch("servicepytan.data.Endpoint")
    def test_get_sold_estimates_between(self, MockEndpoint, mock_convert_date):
        mock_endpoint_instance = MockEndpoint.return_value
        mock_endpoint_instance.get_all.return_value = [{"id": 4}]

        data_service = DataService(conn=self.conn)
        result = data_service.get_sold_estimates_between("start", "end")

        MockEndpoint.assert_called_with("sales", "estimates")
        mock_endpoint_instance.get_all.assert_called_once_with(
            {"active": "True", "soldAfter": "start", "soldBefore": "end"}
        )
        self.assertEqual(result, [{"id": 4}])

    @patch.object(DataService, "get_sold_estimates_between")
    def test_get_total_sales_between(
        self, mock_get_estimates, mock_convert_date
    ):
        mock_get_estimates.return_value = [
            {"items": [{"total": 100}, {"total": 50}]},
            {"items": [{"total": 200}]},
        ]

        data_service = DataService(conn=self.conn)
        total_sales = data_service.get_total_sales_between("start", "end")

        self.assertEqual(total_sales, 350)
        mock_get_estimates.assert_called_once_with("start", "end")

    @patch("servicepytan.data.Endpoint")
    def test_get_purchase_orders_created_between(
        self, MockEndpoint, mock_convert_date
    ):
        mock_endpoint_instance = MockEndpoint.return_value
        mock_endpoint_instance.get_all.return_value = [{"id": 5}]

        data_service = DataService(conn=self.conn)
        result = data_service.get_purchase_orders_created_between(
            "start", "end"
        )

        MockEndpoint.assert_called_with("inventory", "purchase-orders")
        mock_endpoint_instance.get_all.assert_called_once_with(
            {"createdOnOrAfter": "start", "createdBefore": "end"}
        )
        self.assertEqual(result, [{"id": 5}])

    @patch("servicepytan.data.Endpoint")
    def test_get_jobs_modified_between(self, MockEndpoint, mock_convert_date):
        mock_endpoint_instance = MockEndpoint.return_value
        mock_endpoint_instance.get_all.return_value = [{"id": 6}]

        data_service = DataService(conn=self.conn)
        result = data_service.get_jobs_modified_between("start", "end")

        MockEndpoint.assert_called_with("jpm", "jobs")
        mock_endpoint_instance.get_all.assert_called_once_with(
            {"modifiedOnOrAfter": "start", "modifiedBefore": "end"}
        )
        self.assertEqual(result, [{"id": 6}])

    @patch("servicepytan.data.Endpoint")
    def test_get_employees(self, MockEndpoint, mock_convert_date):
        mock_endpoint_instance = MockEndpoint.return_value
        mock_endpoint_instance.get_all.return_value = [{"name": "John Doe"}]

        data_service = DataService(conn=self.conn)
        result = data_service.get_employees(active="False")

        MockEndpoint.assert_called_with("settings", "employees")
        mock_endpoint_instance.get_all.assert_called_once_with(
            {"active": "False"}
        )
        self.assertEqual(result, [{"name": "John Doe"}])

    @patch("servicepytan.data.Endpoint")
    def test_get_technicians(self, MockEndpoint, mock_convert_date):
        mock_endpoint_instance = MockEndpoint.return_value
        mock_endpoint_instance.get_all.return_value = [{"name": "Jane Tech"}]

        data_service = DataService(conn=self.conn)
        result = data_service.get_technicians(active="True")

        MockEndpoint.assert_called_with("settings", "technicians")
        mock_endpoint_instance.get_all.assert_called_once_with(
            {"active": "True"}
        )
        self.assertEqual(result, [{"name": "Jane Tech"}])

    @patch("servicepytan.data.Endpoint")
    def test_get_tag_types(self, MockEndpoint, mock_convert_date):
        mock_endpoint_instance = MockEndpoint.return_value
        mock_endpoint_instance.get_all.return_value = [{"name": "Lead"}]

        data_service = DataService(conn=self.conn)
        result = data_service.get_tag_types(active="True")

        MockEndpoint.assert_called_with("settings", "tag-types")
        mock_endpoint_instance.get_all.assert_called_once_with(
            {"active": "True"}
        )
        self.assertEqual(result, [{"name": "Lead"}])

    @patch("servicepytan.data.Endpoint")
    def test_get_business_units(self, MockEndpoint, mock_convert_date):
        mock_endpoint_instance = MockEndpoint.return_value
        mock_endpoint_instance.get_all.return_value = [{"name": "Plumbing"}]

        data_service = DataService(conn=self.conn)
        result = data_service.get_business_units(active="True")

        MockEndpoint.assert_called_with("settings", "business-units")
        mock_endpoint_instance.get_all.assert_called_once_with(
            {"active": "True"}
        )
        self.assertEqual(result, [{"name": "Plumbing"}])


if __name__ == "__main__":
    unittest.main()
