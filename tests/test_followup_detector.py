import unittest

from app.memory.followup_detector import FollowUpDetector


class TestFollowUpDetector(unittest.TestCase):

    def setUp(self):
        self.detector = FollowUpDetector()

    def test_what_about_question(self):
        result = self.detector.is_follow_up(
            "What about Quantity?",
            "What is total Sales?"
        )

        self.assertTrue(result)

    def test_how_about_question(self):
        result = self.detector.is_follow_up(
            "How about Profit?",
            "What is total Sales?"
        )

        self.assertTrue(result)

    def test_and_quantity_question(self):
        result = self.detector.is_follow_up(
            "And Quantity?",
            "What is total Sales?"
        )

        self.assertTrue(result)

    def test_new_question(self):
        result = self.detector.is_follow_up(
            "Show the distribution of Quantity.",
            "What is total Sales?"
        )

        self.assertFalse(result)

    def test_no_previous_question(self):
        result = self.detector.is_follow_up(
            "What about Quantity?",
            None
        )

        self.assertFalse(result)

    def test_empty_question(self):
        result = self.detector.is_follow_up(
            "",
            "What is total Sales?"
        )

        self.assertFalse(result)

    def test_also_question(self):
        result = self.detector.is_follow_up(
            "Also Profit?",
            "What is total Sales?"
        )

        self.assertTrue(result)

    def test_case_insensitive_question(self):
        result = self.detector.is_follow_up(
            "WHAT ABOUT QUANTITY?",
            "What is total Sales?"
        )

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()