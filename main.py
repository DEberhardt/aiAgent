import os, sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=api_key)

question = sys.argv[1] if len(sys.argv) > 1 else None
if not question:
    sys.exit(1)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=question
)
print(response.text)

print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
