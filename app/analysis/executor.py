import io
from contextlib import redirect_stdout


SAFE_BUILTINS = {
    "len": len,
    "sum": sum,
    "min": min,
    "max": max,
    "abs": abs,
    "round": round
}


def execute_code(code, df):
    try:
        execution_environment = {
            "df": df,
            "__builtins__": SAFE_BUILTINS
        }

        output = io.StringIO()

        with redirect_stdout(output):
            exec(code, execution_environment)

        result = execution_environment.get("result")

        if result is None:
            return {
                "success": False,
                "result": None,
                "output": output.getvalue(),
                "error": "No result was produced by the generated code.",
                "error_type": "MissingResult"
            }

        return {
            "success": True,
            "result": result,
            "output": output.getvalue(),
            "error": None,
            "error_type": None
        }

    except Exception as e:
        return {
            "success": False,
            "result": None,
            "output": "",
            "error": str(e),
            "error_type": type(e).__name__
        }


