import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app import activities, app


class ActivityRouteTests(unittest.TestCase):
    def setUp(self):
        self.activities = patch.dict(
            activities,
            {
                "Test Club": {
                    "description": "A test activity",
                    "schedule": "Mondays",
                    "max_participants": 10,
                    "participants": ["student@example.com"],
                }
            },
            clear=True,
        )
        self.activities.start()
        self.addCleanup(self.activities.stop)
        self.client = TestClient(app)

    def test_get_activities_returns_activity_data(self):
        response = self.client.get("/activities")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "Test Club": {
                    "description": "A test activity",
                    "schedule": "Mondays",
                    "max_participants": 10,
                    "participants": ["student@example.com"],
                }
            },
        )

    def test_root_redirects_to_static_index(self):
        response = self.client.get("/", follow_redirects=False)

        self.assertEqual(response.status_code, 307)
        self.assertEqual(response.headers["location"], "/static/index.html")


if __name__ == "__main__":
    unittest.main()
