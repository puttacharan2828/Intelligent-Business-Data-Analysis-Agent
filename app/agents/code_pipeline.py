from app.agents.code_generator import generate_code
from app.agents.code_validator import validate_code


def generate_valid_code(plan):
    code = generate_code(plan)

    if not validate_code(code):
        raise ValueError("Generated code is invalid.")

    return code