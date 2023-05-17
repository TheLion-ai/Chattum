"""Tests for the backend application."""
import unittest

from app import app
from fastapi.testclient import TestClient


class Test01HealthCheck(unittest.TestCase):
    """Test the health check endpoint."""

    def setUp(self) -> None:
        """Set up the test client."""
        self.test_client = TestClient(app)

    def test_health_check(self) -> None:
        """Test the health check endpoint."""
        response = self.test_client.get("/health_check")
        assert response.status_code == 200


if __name__ == "__main__":
    unittest.main()
