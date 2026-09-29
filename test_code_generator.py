from app.agents.code_generator import generate_code


plan1 = {
    "analysis_type": "summary",
    "target_column": "Sales"
}

plan2 = {
    "analysis_type": "distribution",
    "target_column": "Sales"
}

plan3 = {
    "analysis_type": "aggregation",
    "target_column": "Sales",
    "operation": "sum"
}

plan4 = {
    "analysis_type": "aggregation",
    "target_column": "Sales",
    "operation": "mean"
}

plan5 = {
    "analysis_type": "relationship",
    "target_column": "Sales",
    "group_by": "Profit"
}

plan6 = {
    "analysis_type": "aggregation",
    "target_column": "Sales",
    "group_by": "Region",
    "operation": "sum",
    "filter": None
}

plan7 = {
    "analysis_type": "aggregation",
    "target_column": "Sales",
    "group_by": "Category",
    "operation": "sum",
    "filter": {
        "column": "Region",
        "value": "East"
    }
}

plan8 = {
    "analysis_type": "aggregation",
    "target_column": "Sales",
    "group_by": None,
    "operation": "sum",
    "filter": None,
    "time": 2024
}

print("\nTime-Based - Sales in 2024:")
print(generate_code(plan8))


print("Summary:")
print(generate_code(plan1))

print("\nDistribution:")
print(generate_code(plan2))

print("\nAggregation - Sum:")
print(generate_code(plan3))

print("\nAggregation - Mean:")
print(generate_code(plan4))

print("\nRelationship - Sales and Profit:")
print(generate_code(plan5))

print("\nGrouping - Sales by Region:")
print(generate_code(plan6))

print("\nFiltering + Grouping:")
print(generate_code(plan7))