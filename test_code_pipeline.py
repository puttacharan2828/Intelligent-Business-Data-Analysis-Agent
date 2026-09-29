from app.agents.code_pipeline import generate_valid_code


plan = {
    "analysis_type": "aggregation",
    "target_column": "Sales",
    "group_by": "Region",
    "operation": "sum",
    "filter": None,
    "time": None
}

code = generate_valid_code(plan)

print("Generated and Validated Code:")
print(code)