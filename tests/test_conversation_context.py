import unittest

from app.memory.conversation_memory import ConversationMemory
from app.memory.conversation_context import ConversationContext


class TestConversationContext(unittest.TestCase):

    def setUp(self):
        self.memory = ConversationMemory()
        self.context = ConversationContext(self.memory)

    def test_new_question(self):

        result = self.context.resolve_question(
            "What is total Sales?"
        )

        self.assertFalse(result["is_follow_up"])
        self.assertEqual(
            result["resolved_question"],
            "What is total Sales?"
        )

    def test_follow_up_question(self):

        self.memory.add(
            "What is total Sales?",
            125000,
            "Total Sales is 125000."
        )

        result = self.context.resolve_question(
            "What about Quantity?"
        )

        self.assertTrue(result["is_follow_up"])

        self.assertEqual(
            result["resolved_question"],
            "What is total Quantity?"
        )

    def test_grouped_follow_up(self):

        self.memory.add(
            "What is total Sales by Category?",
            None,
            "Sales grouped by Category."
        )

        result = self.context.resolve_question(
            "What about Quantity?"
        )

        self.assertTrue(result["is_follow_up"])

        self.assertEqual(
            result["resolved_question"],
            "What is total Quantity by Category?"
        )

    def test_previous_question_is_returned(self):

        self.memory.add(
            "What is total Sales?",
            125000,
            "Total Sales is 125000."
        )

        result = self.context.resolve_question(
            "Show the distribution of Quantity."
        )

        self.assertEqual(
            result["previous_question"],
            "What is total Sales?"
        )

    def test_and_follow_up(self):

        memory = ConversationMemory()

        memory.add(
            "What is total Sales by Category?",
            125000,
            "Highest category is Hyderabad."
        )

        context = ConversationContext(memory)

        result = context.resolve_question(
            "And Profit?"
        )

        self.assertTrue(result["is_follow_up"])

        self.assertEqual(
            result["resolved_question"],
            "What is total Profit by Category?"
        )


if __name__ == "__main__":
    unittest.main()