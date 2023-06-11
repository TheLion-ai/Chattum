"""Tests for the backend application."""
import pytest


def test_health_check(test_client) -> None:
    """Test the health check endpoint."""
    response = test_client.get("/health_check")
    assert response.status_code == 200
