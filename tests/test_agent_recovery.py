import unittest
import pandas as pd
from unittest.mock import patch

from app.agents.agent import AnalysisAgent


class TestAgentRecovery(unittest.TestCase):

    def test_recovery_attempted_on_execution_error(self):

        agent = AnalysisAgent()

        agent.state.dataset = pd.DataFrame(
            columns=["Product", "Category", "Sales", "Quantity"]
        )

        execution = {
            "success": False,
            "result": None,
            "output": "",
            "error": "Test execution error",
            "error_type": "KeyError"
        }

        result = agent.recover(execution)

        self.assertFalse(result)
        self.assertTrue(agent.state.recovery_attempted)

        self.assertEqual(
            agent.state.error,
            "Analysis failed because the generated code "
            "used a column that does not exist. "
            "Available columns: Product, Category, Sales, Quantity."
        )

    def test_recovery_handles_key_error(self):

        agent = AnalysisAgent()

        agent.state.dataset = pd.DataFrame(
            columns=["Product", "Category", "Sales", "Quantity"]
        )

        execution = {
            "success": False,
            "result": None,
            "output": "",
            "error": "'UnknownColumn'",
            "error_type": "KeyError"
        }

        result = agent.recover(execution)

        self.assertFalse(result)
        self.assertTrue(agent.state.recovery_attempted)

        self.assertEqual(
            agent.state.error,
            "Analysis failed because the generated code "
            "used a column that does not exist. "
            "Available columns: Product, Category, Sales, Quantity."
        )

    def test_recovery_retries_execution(self):

        agent = AnalysisAgent()

        agent.state.dataset = pd.DataFrame(
            columns=["Product", "Category", "Sales", "Quantity"]
        )

        execution = {
            "success": False,
            "result": None,
            "output": "",
            "error": "'UnknownColumn'",
            "error_type": "KeyError"
        }

        result = agent.recover(execution)

        self.assertTrue(agent.state.recovery_attempted)
        self.assertFalse(result)

    @patch("app.agents.agent.execute_code")
    def test_recovery_retries_execution_with_mock(self, mock_execute):

        mock_execute.side_effect = [
            {
                "success": False,
                "result": None,
                "output": "",
                "error": "Temporary error",
                "error_type": "KeyError"
            },
            {
                "success": True,
                "result": 125000,
                "output": "",
                "error": None,
                "error_type": None
            }
        ]

        agent = AnalysisAgent()

        agent.state.dataset = pd.DataFrame(
            columns=["Product", "Category", "Sales", "Quantity"]
        )

        execution = mock_execute()

        agent.recover(execution)

        self.assertTrue(agent.state.recovery_attempted)


    def test_recovery_handles_missing_result(self):

        agent = AnalysisAgent()

        agent.state.dataset = pd.DataFrame(
            columns=["Product", "Category", "Sales", "Quantity"]
        )

        execution = {
            "success": False,
            "result": None,
            "output": "",
            "error": "No result was produced by the generated code.",
            "error_type": "MissingResult"
        }

        result = agent.recover(execution)

        self.assertFalse(result)
        self.assertTrue(agent.state.recovery_attempted)

        self.assertEqual(
            agent.state.error,
            "Analysis failed because the generated code "
            "did not produce a result."
        )

    @patch("app.agents.agent.execute_code")
    def test_agent_run_attempts_recovery(self, mock_execute):

        mock_execute.return_value = {
            "success": False,
            "result": None,
            "output": "",
            "error": "'UnknownColumn'",
            "error_type": "KeyError"
        }

        agent = AnalysisAgent()

        df = pd.DataFrame({
            "Product": ["Laptop", "Phone"],
            "Category": ["Electronics", "Electronics"],
            "Sales": [50000, 30000],
            "Quantity": [10, 20]
        })

        result = agent.run(
            "What is total Sales?",
            df,
            df.columns.tolist()
        )

        self.assertTrue(result.recovery_attempted)
        self.assertEqual(result.error_type, "execution_error")
        self.assertEqual(result.specific_error_type, "KeyError")


if __name__ == "__main__":
    unittest.main()