import unittest
from unittest.mock import patch
from servicepytan.summary import get_booked_jobs_by_agent


class TestSummary(unittest.TestCase):

    @patch("servicepytan.summary.DataService")
    def test_get_booked_jobs_by_agent_incomplete(self, MockDataService):
        """
        Test that get_booked_jobs_by_agent runs without error.
        Note: This function is currently incomplete. This test just ensures
        it calls the DataService methods as expected. The test should be
        updated when the function is fully implemented.
        """
        mock_data_service_instance = MockDataService.return_value
        mock_data_service_instance.get_jobs_created_between.return_value = []
        mock_data_service_instance.get_employees.return_value = []

        conn = {"config": "data"}
        result = get_booked_jobs_by_agent("start", "end", conn=conn)

        # The function should call DataService with the connection
        MockDataService.assert_called_once_with(conn=conn)

        # It should call get_jobs_created_between
        mock_data_service_instance.get_jobs_created_between.assert_called_once_with(
            "start", "end"
        )

        # It should call get_employees
        mock_data_service_instance.get_employees.assert_called_once()

        # The function currently returns None because it's incomplete
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
