from app.agents.code_validator import validate_code

valid_code = 'df["Sales"].sum()'
invalid_code = 'df["Sales".sum()'

print("Valid code:")
print(validate_code(valid_code))

print("\nInvalid code:")
print(validate_code(invalid_code))