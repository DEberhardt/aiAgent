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

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Importing function declarations
from functions.get_files_info import schema_get_files_info

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

# Configuration
config = types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt,
)

# Defining Model
model = "gemini-2.0-flash-001"

# Sending request
response = client.models.generate_content(
    model=model, contents=messages, config=config
)

# handling response
if response.function_calls:
    for fc in response.function_calls:
        print(f"Calling function: {fc.name}({fc.args})")
else:
    print(response.text)


# handling verbose output
if "--verbose" in sys.argv:
    print(f"User prompt: {question}")
    # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
