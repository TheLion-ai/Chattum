import unittest

from api import app
from fastapi.testclient import TestClient

unittest.TestLoader.sortTestMethodsUsing = None


class Test01HealthCheck(unittest.TestCase):
    def setUp(self) -> None:
        self.test_client = TestClient(app)

    def test_health_check(self):
        response = self.test_client.get("/health_check")
        assert response.status_code == 200


if __name__ == "__main__":
    unittest.main()
