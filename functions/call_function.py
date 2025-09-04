from functions.registry import function_declarations
from google.genai import types
from config import WORKING_DIR


def call_function(function_call_part, verbose=False):
    name = function_call_part.name
    args = dict(function_call_part.args or {})
    if verbose:
        print(f"Calling function: {name}({args})")
    else:
        print(f" - Calling function: {name}")

    func = function_declarations.get(name)
    if not func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name, response={"error": f"Unknown function: {name}"}
                )
            ],
        )

    args["working_directory"] = WORKING_DIR
    try:
        result = func(**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name, response={"result": result}
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Function {name} returned an error: {e}"},
                )
            ],
        )
