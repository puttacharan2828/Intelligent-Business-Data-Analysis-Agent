import unittest

from app.agents.agent_state import AgentState


class TestAgentState(unittest.TestCase):

    def test_error_type_initially_none(self):
        state = AgentState()

        self.assertIsNone(state.error_type)

    def test_specific_error_type(self):
        state = AgentState()

        state.error_type = "execution_error"
        state.specific_error_type = "KeyError"

        self.assertEqual(
            state.error_type,
            "execution_error"
        )

        self.assertEqual(
            state.specific_error_type,
            "KeyError"
        )


if __name__ == "__main__":
    unittest.main()