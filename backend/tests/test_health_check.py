"""Tests for the backend application."""

import pytest


def test_health_check(test_client, api_key) -> None:
    """Test the health check endpoint."""
    response = test_client.get("/health_check", headers={"X-API-Key": api_key})
    assert response.status_code == 200
