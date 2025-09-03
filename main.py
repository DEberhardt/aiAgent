import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=api_key)

question = sys.argv[1] if len(sys.argv) > 1 else None
if not question:
    sys.exit(1)

# We should have a question to ask now
messages = [
    types.Content(role="user", parts=[types.Part(text=question)]),
]

# Adding System Prompt for later use
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


# Configuration
from functions.call_function import call_function
from functions.registry import available_functions

config = types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt,
)

# Defining Model
model = "gemini-2.0-flash-001"

# Sending request
response = client.models.generate_content(model=model, contents=messages, config=config)

# handling response
if response.function_calls:
    for fc in response.function_calls:
        function_call_result = call_function(fc, verbose="--verbose" in sys.argv)

        # Must have .parts[0].function_response.response
        try:
            resp = function_call_result.parts[0].function_response.response
        except Exception:
            raise RuntimeError(
                "Fatal: tool call returned no function_response.response"
            )

        if "--verbose" in sys.argv:
            print(f"-> {resp}")
else:
    print(response.text)


# handling verbose output
if "--verbose" in sys.argv:
    print(f"User prompt: {question}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
