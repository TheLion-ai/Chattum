import unittest

from fastapi.testclient import TestClient

from api import app

unittest.TestLoader.sortTestMethodsUsing = None


class Test01HealthCheck(unittest.TestCase):
    def setUp(self) -> None:
        self.test_client = TestClient(app)

    def test_health_check(self):
        response = self.test_client.get("/health_check")
        assert response.status_code == 300


if __name__ == "__main__":
    unittest.main()
