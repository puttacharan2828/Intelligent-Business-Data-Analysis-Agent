import unittest

from app.memory.conversation_memory import ConversationMemory


class TestConversationMemory(unittest.TestCase):

    def test_empty_memory(self):
        memory = ConversationMemory()

        self.assertEqual(memory.get_history(), [])
        self.assertIsNone(memory.get_last())

    def test_add_and_get_last(self):
        memory = ConversationMemory()

        memory.add(
            "What is total Sales?",
            125000,
            "Total Sales is 125000."
        )

        last = memory.get_last()

        self.assertEqual(last["question"], "What is total Sales?")
        self.assertEqual(last["result"], 125000)
        self.assertEqual(
            last["interpretation"],
            "Total Sales is 125000."
        )

    def test_multiple_entries(self):
        memory = ConversationMemory()

        memory.add(
            "What is total Sales?",
            125000,
            "Total Sales is 125000."
        )

        memory.add(
            "What is total Quantity?",
            500,
            "Total Quantity is 500."
        )

        self.assertEqual(len(memory.get_history()), 2)
        self.assertEqual(
            memory.get_last()["question"],
            "What is total Quantity?"
        )

    def test_get_previous_question(self):
        memory = ConversationMemory()

        memory.add(
            "What is total Sales?",
            125000,
            "Total Sales is 125000."
        )

        self.assertEqual(
            memory.get_previous_question(),
            "What is total Sales?"
        )

    def test_get_previous_result_and_interpretation(self):
        memory = ConversationMemory()

        memory.add(
            "What is total Sales?",
            125000,
            "Total Sales is 125000."
        )

        self.assertEqual(
            memory.get_previous_result(),
            125000
        )

        self.assertEqual(
            memory.get_previous_interpretation(),
            "Total Sales is 125000."
        )

    def test_clear_memory(self):
        memory = ConversationMemory()

        memory.add(
            "What is total Sales?",
            125000,
            "Total Sales is 125000."
        )

        memory.clear()

        self.assertEqual(memory.get_history(), [])
        self.assertIsNone(memory.get_last())

    def test_add_stores_follow_up_information(self):

        memory = ConversationMemory()

        memory.add(
            "What is total Quantity by Category?",
            100,
            "Highest category has 50.",
            is_follow_up=True,
            original_question="What about Quantity?"
        ) 

        last = memory.get_last()

        self.assertTrue(last["is_follow_up"])
        self.assertEqual(
            last["original_question"],
            "What about Quantity?"
        )


if __name__ == "__main__":
    unittest.main()