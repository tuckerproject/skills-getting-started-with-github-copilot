import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app import activities, app


class UnregisterTests(unittest.TestCase):
    def setUp(self):
        self.activities = patch.dict(
            activities,
            {
                "Test Club": {
                    "participants": ["student@example.com", "other@example.com", "student@example.com"]
                },
                "Other Club": {"participants": ["student@example.com"]},
            },
            clear=True,
        )
        self.activities.start()
        self.addCleanup(self.activities.stop)
        self.client = TestClient(app)

    def test_unregister_removes_all_matching_entries_only_from_selected_activity(self):
        response = self.client.delete(
            "/activities/Test%20Club/signup", params={"email": "student@example.com"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(activities["Test Club"]["participants"], ["other@example.com"])
        self.assertEqual(activities["Other Club"]["participants"], ["student@example.com"])

    def test_unregister_unknown_activity(self):
        response = self.client.delete(
            "/activities/Missing/signup", params={"email": "student@example.com"}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Activity not found")

    def test_unregister_unknown_participant(self):
        response = self.client.delete(
            "/activities/Test%20Club/signup", params={"email": "missing@example.com"}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Student not signed up for this activity")
        self.assertEqual(len(activities["Test Club"]["participants"]), 3)


if __name__ == "__main__":
    unittest.main()
