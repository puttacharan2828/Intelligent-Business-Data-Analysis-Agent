import unittest

from app.memory.context_resolver import ContextResolver


class TestContextResolver(unittest.TestCase):

    def setUp(self):
        self.resolver = ContextResolver()

    def test_what_about(self):
        result = self.resolver.resolve(
            "What about Quantity?",
            "What is total Sales?"
        )

        self.assertEqual(
            result,
            "What is total Quantity?"
        )

    def test_how_about(self):
        result = self.resolver.resolve(
            "How about Profit?",
            "What is total Sales?"
        )

        self.assertEqual(
            result,
            "What is total Profit?"
        )

    def test_and_question(self):
        result = self.resolver.resolve(
            "And Quantity?",
            "What is total Sales?"
        )

        self.assertEqual(
            result,
            "What is total Quantity?"
        )

    def test_also_question(self):
        result = self.resolver.resolve(
            "Also Profit?",
            "What is total Sales?"
        )

        self.assertEqual(
            result,
            "What is total Profit?"
        )

    def test_grouped_question(self):
        result = self.resolver.resolve(
            "What about Quantity?",
            "What is total Sales by Category?"
        )

        self.assertEqual(
            result,
            "What is total Quantity by Category?"
        )

    def test_no_previous_question(self):
        result = self.resolver.resolve(
            "What about Quantity?",
            None
        )

        self.assertEqual(
            result,
            "What about Quantity?"
        )

    def test_new_question(self):
        result = self.resolver.resolve(
            "Show the distribution of Quantity.",
            "What is total Sales?"
        )

        self.assertEqual(
            result,
            "Show the distribution of Quantity."
        )


if __name__ == "__main__":
    unittest.main()