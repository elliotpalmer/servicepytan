"""Tests for authentication module."""

import json
import os
import tempfile
import time
import unittest
from unittest.mock import Mock, patch

import pytest

from servicepytan.auth import (
    ApiEnvironment,
    clear_token_cache,
    get_api_root_url,
    get_app_key,
    get_auth_headers,
    get_auth_root_url,
    get_auth_token,
    get_tenant_id,
    request_auth_token,
    servicepytan_connect,
)


class TestApiEnvironment(unittest.TestCase):
    """Test API environment configuration."""

    def test_get_auth_root_url_production(self):
        """Test production auth URL."""
        url = get_auth_root_url(ApiEnvironment.PRODUCTION)
        self.assertEqual(url, "https://auth.servicetitan.io")

    def test_get_auth_root_url_integration(self):
        """Test integration auth URL."""
        url = get_auth_root_url(ApiEnvironment.INTEGRATION)
        self.assertEqual(url, "https://auth-integration.servicetitan.io")

    def test_get_auth_root_url_invalid(self):
        """Test invalid environment raises ValueError."""
        with self.assertRaises(ValueError):
            get_auth_root_url("invalid")

    def test_get_api_root_url_production(self):
        """Test production API URL."""
        url = get_api_root_url(ApiEnvironment.PRODUCTION)
        self.assertEqual(url, "https://api.servicetitan.io")

    def test_get_api_root_url_integration(self):
        """Test integration API URL."""
        url = get_api_root_url(ApiEnvironment.INTEGRATION)
        self.assertEqual(url, "https://api-integration.servicetitan.io")

    def test_get_api_root_url_invalid(self):
        """Test invalid environment raises ValueError."""
        with self.assertRaises(ValueError):
            get_api_root_url("invalid")


class TestServicePytanConnect(unittest.TestCase):
    """Test connection configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_config = {
            "SERVICETITAN_APP_KEY": "test_app_key",
            "SERVICETITAN_TENANT_ID": "test_tenant_id",
            "SERVICETITAN_CLIENT_ID": "test_client_id",
            "SERVICETITAN_CLIENT_SECRET": "test_client_secret",
        }

    def test_servicepytan_connect_with_parameters(self):
        """Test connection with explicit parameters."""
        conn = servicepytan_connect(
            api_environment="production",
            app_key="test_app_key",
            tenant_id="test_tenant_id",
            client_id="test_client_id",
            client_secret="test_client_secret",
        )

        self.assertEqual(conn["SERVICETITAN_APP_KEY"], "test_app_key")
        self.assertEqual(conn["SERVICETITAN_TENANT_ID"], "test_tenant_id")
        self.assertEqual(conn["SERVICETITAN_CLIENT_ID"], "test_client_id")
        self.assertEqual(conn["SERVICETITAN_CLIENT_SECRET"], "test_client_secret")
        self.assertEqual(conn["auth_root"], "https://auth.servicetitan.io")
        self.assertEqual(conn["api_root"], "https://api.servicetitan.io")

    def test_servicepytan_connect_with_config_file(self):
        """Test connection with config file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.valid_config, f)
            config_file = f.name

        try:
            conn = servicepytan_connect(config_file=config_file)
            self.assertEqual(conn["SERVICETITAN_APP_KEY"], "test_app_key")
            self.assertEqual(conn["SERVICETITAN_TENANT_ID"], "test_tenant_id")
        finally:
            os.unlink(config_file)

    def test_servicepytan_connect_missing_file(self):
        """Test connection with non-existent config file."""
        with self.assertRaises(ValueError) as cm:
            servicepytan_connect(config_file="nonexistent.json")
        self.assertIn("Configuration file not found", str(cm.exception))

    def test_servicepytan_connect_invalid_json(self):
        """Test connection with invalid JSON config file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json")
            config_file = f.name

        try:
            with self.assertRaises(ValueError) as cm:
                servicepytan_connect(config_file=config_file)
            self.assertIn("Invalid JSON", str(cm.exception))
        finally:
            os.unlink(config_file)

    def test_servicepytan_connect_missing_credentials(self):
        """Test connection with missing required credentials."""
        with self.assertRaises(ValueError) as cm:
            servicepytan_connect(
                app_key="test_app_key",
                # Missing other required fields
            )
        self.assertIn("Missing required credentials", str(cm.exception))

    def test_servicepytan_connect_empty_credentials(self):
        """Test connection with empty credentials."""
        with self.assertRaises(ValueError) as cm:
            servicepytan_connect(
                app_key="test_app_key",
                tenant_id="",  # Empty
                client_id="test_client_id",
                client_secret="test_client_secret",
            )
        self.assertIn("Empty credentials", str(cm.exception))

    @patch.dict(os.environ, {
        'SERVICETITAN_APP_KEY': 'env_app_key',
        'SERVICETITAN_TENANT_ID': 'env_tenant_id',
        'SERVICETITAN_CLIENT_ID': 'env_client_id',
        'SERVICETITAN_CLIENT_SECRET': 'env_client_secret',
    })
    def test_servicepytan_connect_from_environment(self):
        """Test connection from environment variables."""
        conn = servicepytan_connect()
        self.assertEqual(conn["SERVICETITAN_APP_KEY"], "env_app_key")
        self.assertEqual(conn["SERVICETITAN_TENANT_ID"], "env_tenant_id")


class TestTokenCaching(unittest.TestCase):
    """Test authentication token caching."""

    def setUp(self):
        """Set up test fixtures."""
        clear_token_cache()  # Clear cache before each test
        self.conn = {
            "SERVICETITAN_CLIENT_ID": "test_client_id",
            "SERVICETITAN_CLIENT_SECRET": "test_client_secret",
            "SERVICETITAN_APP_KEY": "test_app_key",
            "auth_root": "https://auth.servicetitan.io",
        }

    def tearDown(self):
        """Clean up after tests."""
        clear_token_cache()

    @patch('servicepytan.auth.request_auth_token')
    def test_get_auth_token_caching(self, mock_request):
        """Test that tokens are cached and reused."""
        mock_response = {
            "access_token": "test_token",
            "expires_in": 3600,
            "expires_at": time.time() + 3600
        }
        mock_request.return_value = mock_response

        # First call should make request
        token1 = get_auth_token(self.conn)
        self.assertEqual(token1, "Bearer test_token")
        self.assertEqual(mock_request.call_count, 1)

        # Second call should use cache
        token2 = get_auth_token(self.conn)
        self.assertEqual(token2, "Bearer test_token")
        self.assertEqual(mock_request.call_count, 1)  # No additional calls

    @patch('servicepytan.auth.request_auth_token')
    def test_get_auth_token_expiration(self, mock_request):
        """Test that expired tokens are refreshed."""
        # First token (expired)
        expired_token = {
            "access_token": "expired_token",
            "expires_in": 3600,
            "expires_at": time.time() - 100  # Expired
        }
        
        # New token
        new_token = {
            "access_token": "new_token",
            "expires_in": 3600,
            "expires_at": time.time() + 3600
        }
        
        mock_request.side_effect = [expired_token, new_token]

        # First call
        token1 = get_auth_token(self.conn)
        self.assertEqual(token1, "Bearer expired_token")

        # Second call should refresh expired token
        token2 = get_auth_token(self.conn)
        self.assertEqual(token2, "Bearer new_token")
        self.assertEqual(mock_request.call_count, 2)

    def test_clear_token_cache_specific(self):
        """Test clearing cache for specific connection."""
        # This is more of an integration test
        clear_token_cache(self.conn)  # Should not raise exception

    def test_clear_token_cache_all(self):
        """Test clearing all cached tokens."""
        clear_token_cache()  # Should not raise exception


@patch('servicepytan.auth.requests.post')
class TestRequestAuthToken(unittest.TestCase):
    """Test token request functionality."""

    def test_request_auth_token_success(self, mock_post):
        """Test successful token request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "test_token",
            "expires_in": 3600
        }
        mock_post.return_value = mock_response

        result = request_auth_token(
            "https://auth.servicetitan.io",
            "client_id",
            "client_secret"
        )

        self.assertEqual(result["access_token"], "test_token")
        self.assertEqual(result["expires_in"], 3600)
        self.assertIn("expires_at", result)

    def test_request_auth_token_failure(self, mock_post):
        """Test failed token request."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_response.raise_for_status.side_effect = Exception("HTTP 401")
        mock_post.return_value = mock_response

        with self.assertRaises(Exception):
            request_auth_token(
                "https://auth.servicetitan.io",
                "invalid_client",
                "invalid_secret"
            )


class TestCredentialHelpers(unittest.TestCase):
    """Test credential helper functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.conn = {
            "SERVICETITAN_APP_KEY": "test_app_key",
            "SERVICETITAN_TENANT_ID": "test_tenant_id",
        }

    def test_get_app_key(self):
        """Test getting app key from connection."""
        key = get_app_key(self.conn)
        self.assertEqual(key, "test_app_key")

    def test_get_app_key_missing(self):
        """Test getting app key when missing."""
        with self.assertRaises(KeyError):
            get_app_key({})

    def test_get_tenant_id(self):
        """Test getting tenant ID from connection."""
        tenant_id = get_tenant_id(self.conn)
        self.assertEqual(tenant_id, "test_tenant_id")

    def test_get_tenant_id_missing(self):
        """Test getting tenant ID when missing."""
        with self.assertRaises(KeyError):
            get_tenant_id({})

    @patch('servicepytan.auth.get_auth_token')
    def test_get_auth_headers(self, mock_get_token):
        """Test getting authentication headers."""
        mock_get_token.return_value = "Bearer test_token"
        
        headers = get_auth_headers(self.conn)
        
        self.assertEqual(headers["Authorization"], "Bearer test_token")
        self.assertEqual(headers["ST-App-Key"], "test_app_key")


if __name__ == "__main__":
    unittest.main()