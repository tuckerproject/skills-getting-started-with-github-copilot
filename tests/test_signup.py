import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app import activities, app


class SignupTests(unittest.TestCase):
    def setUp(self):
        self.activities = patch.dict(
            activities,
            {
                "Test Club": {
                    "participants": ["existing@example.com"],
                }
            },
            clear=True,
        )
        self.activities.start()
        self.addCleanup(self.activities.stop)
        self.client = TestClient(app)

    def test_signup_adds_student_to_activity(self):
        response = self.client.post(
            "/activities/Test%20Club/signup",
            params={"email": "student@example.com"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"message": "Signed up student@example.com for Test Club"},
        )
        self.assertEqual(
            activities["Test Club"]["participants"],
            ["existing@example.com", "student@example.com"],
        )

    def test_signup_unknown_activity(self):
        response = self.client.post(
            "/activities/Missing/signup",
            params={"email": "student@example.com"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Activity not found")
        self.assertEqual(
            activities["Test Club"]["participants"], ["existing@example.com"]
        )

    def test_signup_student_already_registered(self):
        response = self.client.post(
            "/activities/Test%20Club/signup",
            params={"email": "existing@example.com"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"],
            "Student already signed up for this activity",
        )
        self.assertEqual(
            activities["Test Club"]["participants"], ["existing@example.com"]
        )


if __name__ == "__main__":
    unittest.main()
