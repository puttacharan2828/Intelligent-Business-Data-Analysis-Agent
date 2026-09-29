from app.nlu.question_parser import parse_question
from app.agents.planner import create_analysis_plan
from app.agents.plan_validator import validate_analysis_plan


test_cases = [
    ("What is the total Sales?", ["Sales"]),
    ("What is the average Sales by Region?", ["Sales", "Region"]),
    ("Show the trend in Sales", ["Sales"]),
    ("Show the distribution of Sales", ["Sales"]),
    ("Is Sales related to Profit?", ["Sales", "Profit"])
]


for question, columns in test_cases:

    print("\nQuestion:")
    print(question)

    nlu_result = parse_question(question, columns)

    print("NLU Result:")
    print(nlu_result)

    plan = create_analysis_plan(nlu_result)

    print("Analysis Plan:")
    print(plan.to_dict())

    print("Plan Valid:")
    print(validate_analysis_plan(plan))

from app.agents.analysis_plan import AnalysisPlan

print("\nInvalid Plan Test:")

invalid_plan = AnalysisPlan(
    analysis_type="grouped_aggregation",
    target_column="Sales",
    group_by=None,
    operation="mean"
)

print("Plan Valid:")
print(validate_analysis_plan(invalid_plan))