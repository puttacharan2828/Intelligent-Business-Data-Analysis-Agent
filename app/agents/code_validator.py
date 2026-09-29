import ast


def validate_code(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False