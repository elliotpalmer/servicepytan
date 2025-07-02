"""Tests for requests module."""

import unittest
from unittest.mock import Mock, patch

from servicepytan.requests import Endpoint


class TestEndpoint(unittest.TestCase):
    """Test Endpoint class functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.conn = {
            'SERVICETITAN_CLIENT_ID': 'test_client',
            'SERVICETITAN_CLIENT_SECRET': 'test_secret',
            'SERVICETITAN_APP_KEY': 'test_app_key',
            'SERVICETITAN_TENANT_ID': 'test_tenant',
            'auth_root': 'https://auth.servicetitan.io',
            'api_root': 'https://api.servicetitan.io'
        }
        self.endpoint = Endpoint("jpm", "jobs", self.conn)

    @patch('servicepytan.requests.request_json_with_retry')
    def test_get_one(self, mock_request):
        """Test get_one method."""
        mock_response = {"id": "12345", "summary": "Test Job"}
        mock_request.return_value = mock_response

        result = self.endpoint.get_one("12345")

        self.assertEqual(result, mock_response)
        mock_request.assert_called_once()
        
        # Check URL construction
        args, kwargs = mock_request.call_args
        self.assertIn("jobs/12345", args[0])
        self.assertEqual(kwargs['request_type'], 'GET')

    @patch('servicepytan.requests.request_json_with_retry')
    def test_get_one_with_modifier(self, mock_request):
        """Test get_one method with modifier."""
        mock_response = [{"id": "note1", "text": "Test note"}]
        mock_request.return_value = mock_response

        result = self.endpoint.get_one("12345", modifier="notes")

        self.assertEqual(result, mock_response)
        
        # Check URL construction includes modifier
        args, kwargs = mock_request.call_args
        self.assertIn("jobs/12345/notes", args[0])

    @patch('servicepytan.requests.request_json_with_retry')
    def test_get_many(self, mock_request):
        """Test get_many method."""
        mock_response = {
            "data": [{"id": "1"}, {"id": "2"}],
            "hasMore": False,
            "totalCount": 2
        }
        mock_request.return_value = mock_response

        result = self.endpoint.get_many({"pageSize": 50})

        self.assertEqual(result, mock_response)
        
        # Check default options are applied
        args, kwargs = mock_request.call_args
        self.assertIn("pageSize", kwargs['options'])

    @patch('servicepytan.requests.request_json_with_retry')
    def test_get_all_single_page(self, mock_request):
        """Test get_all method with single page."""
        mock_response = {
            "data": [{"id": "1"}, {"id": "2"}],
            "hasMore": False,
            "totalCount": 2
        }
        mock_request.return_value = mock_response

        result = self.endpoint.get_all()

        self.assertEqual(result, [{"id": "1"}, {"id": "2"}])
        mock_request.assert_called_once()

    @patch('servicepytan.requests.request_json_with_retry')
    def test_get_all_empty_result(self, mock_request):
        """Test get_all method with empty result."""
        mock_response = {
            "data": [],
            "hasMore": False,
            "totalCount": 0
        }
        mock_request.return_value = mock_response

        result = self.endpoint.get_all()

        self.assertEqual(result, [])
        mock_request.assert_called_once()

    @patch('servicepytan.requests.request_json_with_retry')
    def test_get_all_multiple_pages(self, mock_request):
        """Test get_all method with multiple pages."""
        # First page
        first_response = {
            "data": [{"id": "1"}, {"id": "2"}],
            "hasMore": True,
            "totalCount": 4
        }
        
        # Second page
        second_response = {
            "data": [{"id": "3"}, {"id": "4"}],
            "hasMore": False,
            "totalCount": 4
        }
        
        mock_request.side_effect = [first_response, second_response]

        result = self.endpoint.get_all()

        self.assertEqual(len(result), 4)
        self.assertEqual(result, [{"id": "1"}, {"id": "2"}, {"id": "3"}, {"id": "4"}])
        self.assertEqual(mock_request.call_count, 2)

    @patch('servicepytan.requests.request_json_with_retry')
    def test_create(self, mock_request):
        """Test create method."""
        payload = {"summary": "New Job", "customerId": 123}
        mock_response = {"id": "12345", **payload}
        mock_request.return_value = mock_response

        result = self.endpoint.create(payload)

        self.assertEqual(result, mock_response)
        
        # Check request parameters
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs['request_type'], 'POST')
        self.assertEqual(kwargs['json_payload'], payload)

    @patch('servicepytan.requests.request_json_with_retry')
    def test_update(self, mock_request):
        """Test update method."""
        payload = {"summary": "Updated Job"}
        mock_response = {"id": "12345", **payload}
        mock_request.return_value = mock_response

        result = self.endpoint.update("12345", payload)

        self.assertEqual(result, mock_response)
        
        # Check request parameters
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs['request_type'], 'PUT')
        self.assertEqual(kwargs['payload'], payload)

    @patch('servicepytan.requests.request_json_with_retry')
    def test_update_patch(self, mock_request):
        """Test update method with PATCH."""
        payload = {"summary": "Updated Job"}
        mock_response = {"id": "12345", **payload}
        mock_request.return_value = mock_response

        result = self.endpoint.update("12345", payload, request_type="PATCH")

        self.assertEqual(result, mock_response)
        
        # Check request type
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs['request_type'], 'PATCH')

    @patch('servicepytan.requests.request_json_with_retry')
    def test_delete(self, mock_request):
        """Test delete method."""
        mock_response = {"success": True}
        mock_request.return_value = mock_response

        result = self.endpoint.delete("12345")

        self.assertEqual(result, mock_response)
        
        # Check request parameters
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs['request_type'], 'DEL')
        self.assertIn("jobs/12345", args[0])

    @patch('servicepytan.requests.request_json_with_retry')
    def test_delete_subitem(self, mock_request):
        """Test delete_subitem method."""
        mock_response = {"success": True}
        mock_request.return_value = mock_response

        result = self.endpoint.delete_subitem("12345", "note123", "notes")

        self.assertEqual(result, mock_response)
        
        # Check URL construction
        args, kwargs = mock_request.call_args
        self.assertIn("jobs/12345/notes/note123", args[0])
        self.assertEqual(kwargs['request_type'], 'DEL')

    @patch('servicepytan.requests.request_json_with_retry')
    def test_export_one(self, mock_request):
        """Test export_one method."""
        mock_response = {
            "data": [{"id": "1"}, {"id": "2"}],
            "hasMore": True,
            "continueFrom": "token123"
        }
        mock_request.return_value = mock_response

        result = self.endpoint.export_one("jobs")

        self.assertEqual(result, mock_response)
        
        # Check URL and options
        args, kwargs = mock_request.call_args
        self.assertIn("export/jobs", args[0])
        self.assertIn("from", kwargs['options'])
        self.assertIn("includeRecentChanges", kwargs['options'])

    @patch('servicepytan.requests.request_json_with_retry')
    def test_export_all_single_page(self, mock_request):
        """Test export_all method with single page."""
        mock_response = {
            "data": [{"id": "1"}, {"id": "2"}],
            "hasMore": False,
            "continueFrom": ""
        }
        mock_request.return_value = mock_response

        result = self.endpoint.export_all("jobs")

        self.assertEqual(result, [{"id": "1"}, {"id": "2"}])
        mock_request.assert_called_once()

    @patch('servicepytan.requests.request_json_with_retry')
    def test_export_all_empty_result(self, mock_request):
        """Test export_all method with empty result."""
        mock_response = {
            "data": [],
            "hasMore": False,
            "continueFrom": ""
        }
        mock_request.return_value = mock_response

        result = self.endpoint.export_all("jobs")

        self.assertEqual(result, [])
        mock_request.assert_called_once()

    @patch('servicepytan.requests.request_json_with_retry')
    def test_export_all_multiple_pages(self, mock_request):
        """Test export_all method with multiple pages."""
        # First page
        first_response = {
            "data": [{"id": "1"}, {"id": "2"}],
            "hasMore": True,
            "continueFrom": "token123"
        }
        
        # Second page
        second_response = {
            "data": [{"id": "3"}, {"id": "4"}],
            "hasMore": False,
            "continueFrom": ""
        }
        
        mock_request.side_effect = [first_response, second_response]

        result = self.endpoint.export_all("jobs")

        self.assertEqual(len(result), 4)
        self.assertEqual(result, [{"id": "1"}, {"id": "2"}, {"id": "3"}, {"id": "4"}])
        self.assertEqual(mock_request.call_count, 2)


if __name__ == "__main__":
    unittest.main()