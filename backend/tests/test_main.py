import unittest

from fastapi.testclient import TestClient

from app.main import app


class TestMain(unittest.TestCase):
    def test_root_redirects_to_frontend(self):
        with TestClient(app) as client:
            response = client.get("/", follow_redirects=False)

        self.assertEqual(response.status_code, 307)
        self.assertEqual(response.headers["location"], "http://127.0.0.1:5173/")


if __name__ == "__main__":
    unittest.main()
