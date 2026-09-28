import unittest
from app.nlu.question_parser import parse_question
from app.nlu.nlu_validator import validate_nlu

from app.nlu.intent_detector import detect_intent
from app.nlu.entity_extractor import extract_metric, extract_operation


class TestNLU(unittest.TestCase):

    def test_intent_detection(self):
        self.assertEqual(
            detect_intent("What is the total sales?"),
            "aggregation"
        )

    def test_metric_extraction(self):
        columns = ["Product", "Category", "Sales", "Quantity"]

        self.assertEqual(
            extract_metric("What is the total sales?", columns),
            "Sales"
        )

    def test_operation_extraction(self):
        self.assertEqual(
            extract_operation("What is the average sales?"),
            "mean"
        )

    def test_question_parser(self):
        columns = ["Product", "Category", "Sales", "Quantity"]

        result = parse_question(
            "What is the average sales by category?",
            columns
        )

        self.assertEqual(result["intent"], "aggregation")
        self.assertEqual(result["metric"], "Sales")
        self.assertEqual(result["operation"], "mean")
        self.assertEqual(result["group_by"], "Category")

    def test_nlu_validation(self):
        columns = ["Product", "Category", "Sales", "Quantity"]

        parsed_result = {
            "intent": "aggregation",
            "metric": "Sales",
            "operation": "mean",
            "group_by": "Category",
            "filters": None,
            "time": None
        }

        result = validate_nlu(parsed_result, columns)

        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_missing_metric(self):
        columns = ["Product", "Category", "Sales", "Quantity"]

        parsed_result = {
            "intent": "aggregation",
            "metric": None,
            "operation": "mean",
            "group_by": "Category",
            "filters": None,
            "time": None
        }

        result = validate_nlu(parsed_result, columns)

        self.assertFalse(result["valid"])
        self.assertIn("Metric is missing.", result["errors"])

    def test_invalid_group_by(self):
        columns = ["Product", "Category", "Sales", "Quantity"]

        parsed_result = {
            "intent": "aggregation",
            "metric": "Sales",
            "operation": "mean",
            "group_by": "City",
            "filters": None,
            "time": None
        }

        result = validate_nlu(parsed_result, columns)

        self.assertFalse(result["valid"])
        self.assertIn(
            "Group-by column not found in dataset.",
            result["errors"]
        )

    def test_invalid_filter_column(self):
        columns = ["Product", "Category", "Sales", "Quantity"]

        parsed_result = {
            "intent": "aggregation",
            "metric": "Sales",
            "operation": "sum",
            "group_by": "Category",
            "filters": {
                "column": "City",
                "value": "Hyderabad"
            },
            "time": None
        }

        result = validate_nlu(parsed_result, columns)

        self.assertFalse(result["valid"])
        self.assertIn(
            "Filter column not found in dataset.",
            result["errors"]
        )


if __name__ == "__main__":
    unittest.main()