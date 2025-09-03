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

system_prompt = [
    "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""
]


response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)
print(response.text)

if "--verbose" in sys.argv:
    print(f"User prompt: {question}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
