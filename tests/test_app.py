import unittest

from fastapi import HTTPException

from src import app


class SignupCapacityTests(unittest.TestCase):
    def setUp(self):
        self.activity = app.activities["Chess Club"]
        self.original_participants = self.activity["participants"].copy()
        self.original_max_participants = self.activity["max_participants"]

    def tearDown(self):
        self.activity["participants"] = self.original_participants
        self.activity["max_participants"] = self.original_max_participants

    def test_signup_accepts_last_available_spot(self):
        self.activity["max_participants"] = len(self.activity["participants"]) + 1

        response = app.signup_for_activity("Chess Club", "new-student@mergington.edu")

        self.assertIn("new-student@mergington.edu", self.activity["participants"])
        self.assertEqual(response["message"], "Signed up new-student@mergington.edu for Chess Club")

    def test_signup_rejects_full_activity_without_changing_participants(self):
        self.activity["max_participants"] = len(self.activity["participants"])
        original_participants = self.activity["participants"].copy()

        with self.assertRaises(HTTPException) as raised:
            app.signup_for_activity("Chess Club", "new-student@mergington.edu")

        self.assertEqual(raised.exception.status_code, 400)
        self.assertEqual(raised.exception.detail, "Activity is full")
        self.assertEqual(self.activity["participants"], original_participants)


if __name__ == "__main__":
    unittest.main()
