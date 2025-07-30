"""Tests for Odoo RPC client functionality with real connection."""

import os

import pytest

from prs_commons.odoo.rpc_client import OdooRPCClient

# Skip tests if required environment variables are not set
pytestmark = pytest.mark.skipif(
    not all(
        os.getenv(var)
        for var in ["ODOO_HOST", "ODOO_DB", "ODOO_LOGIN", "ODOO_PASSWORD"]
    ),
    reason="Odoo connection environment variables not set",
)


class TestOdooRPCClientRealConnection:
    """Test suite for OdooRPCClient with real connection."""

    def setup_method(self):
        """Setup test environment before each test method."""
        # Clear the singleton instance before each test
        OdooRPCClient._instance = None
        OdooRPCClient._initialized = False
        self.client = OdooRPCClient()

    def test_successful_connection(self):
        """Test successful connection to Odoo instance."""
        # This will raise an exception if connection fails
        self.client.ensure_connection()

        # Verify client is connected
        print(self.client)
        assert self.client.client is not None

        # Try a simple RPC call to verify connection works
        try:
            # Get server version as a simple test
            version = self.client.client.version
            assert version is not None
            print(f"Connected to Odoo version: {version}")
        except Exception as e:
            pytest.fail(f"Failed to get Odoo version: {str(e)}")

    def test_singleton_pattern(self):
        """Test that only one instance of OdooRPCClient exists."""
        # Create first instance and connect
        client1 = OdooRPCClient()
        client1.ensure_connection()

        # Create second instance
        client2 = OdooRPCClient()

        # Both should be the same instance
        assert client1 is client2

        # Both should be connected
        assert client1.client is not None
        assert client2.client is not None
        assert client1.client is client2.client
        
    def test_logged_in_user(self):
        """Test that we can retrieve the logged-in user's information."""
        # Ensure connection is established
        self.client.ensure_connection()
        
        # Get logged-in user's ID
        user_id = self.client.client.env.user.id
        assert user_id is not None
        
        # Get user details
        user_data = self.client.client.env['res.users'].browse(user_id).read(['name', 'login'])[0]
        
        # Verify the login matches our environment variable
        expected_login = os.getenv("ODOO_LOGIN")
        assert user_data['login'] == expected_login
        
        # Verify we got a name back (should be non-empty)
        assert user_data['name'] is not None
        assert len(user_data['name']) > 0
        
        print(f"Logged in as: {user_data['name']} ({user_data['login']})")
