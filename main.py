import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import MODEL,MAX_ITERATIONS

# Configuration
from functions.call_function import call_function
from functions.registry import available_functions

# Adding System Prompt for later use
system_prompt = """
You are a helpful AI coding agent for a calculator app.
The working directory defined contains all data for this app.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    # We'll iterate up to max_iterations to let the assistant plan, call functions,
    # and then continue the conversation until a final text response is produced.
    max_iterations = MAX_ITERATIONS
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
        except Exception as e:
            print(f"generate_content error on iteration {iteration}: {e}")
            break

        if verbose and getattr(response, "usage_metadata", None):
            try:
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print(
                    "Response tokens:", response.usage_metadata.candidates_token_count
                )
            except Exception:
                # ignore if usage metadata shape differs
                pass

        # Add each candidate's content into the messages so the LLM always has full history
        if getattr(response, "candidates", None):
            for candidate in response.candidates:
                # candidate.content is usually a sequence of types.Content/Part objects
                if hasattr(candidate, "content") and candidate.content:
                    try:
                        for c in candidate.content:
                            # If the part has text, keep it; otherwise fall back to extracting text parts
                            if hasattr(c, "text") and c.text:
                                messages.append(c)
                            else:
                                # Non-text part encountered (e.g. function_call). Use text fallback.
                                text_fallback = extract_text_parts(candidate)
                                if text_fallback:
                                    messages.append(
                                        types.Content(
                                            role="assistant",
                                            parts=[types.Part(text=text_fallback)],
                                        )
                                    )
                                else:
                                    # Last resort: append the raw content object
                                    messages.append(c)
                    except TypeError:
                        # If candidate.content is a single Content-like object or not iterable,
                        # attempt to extract text parts and append a safe assistant Content.
                        text_fallback = extract_text_parts(candidate)
                        if text_fallback:
                            messages.append(
                                types.Content(
                                    role="assistant",
                                    parts=[types.Part(text=text_fallback)],
                                )
                            )
                        else:
                            messages.append(candidate.content)

        # If the model returned plain text, we're done
        if getattr(response, "text", None):
            print(response.text)
            break

        # Handle function calls returned by the model
        function_responses = []
        if getattr(response, "function_calls", None):
            for function_call_part in response.function_calls:
                try:
                    function_call_result = call_function(function_call_part, verbose)
                except Exception as e:
                    print(f"function call failed: {e}")
                    continue

                # Expect the function call result to contain parts with a function_response
                if not getattr(function_call_result, "parts", None) or not getattr(
                    function_call_result.parts[0], "function_response", None
                ):
                    print("empty function call result")
                    continue

                func_resp_text = function_call_result.parts[
                    0
                ].function_response.response
                if verbose:
                    print(f"-> {func_resp_text}")

                # Convert function response into a user role Content and append to messages
                try:
                    messages.append(
                        types.Content(
                            role="user", parts=[types.Part(text=func_resp_text)]
                        )
                    )
                except Exception:
                    # Fallback: append a simple Content-like dict if types.Content fails
                    messages.append(
                        types.Content(
                            role="user", parts=[types.Part(text=str(func_resp_text))]
                        )
                    )

                function_responses.append(func_resp_text)

        # If no function calls and no more candidates/content to process, stop
        if not getattr(response, "function_calls", None) and not getattr(
            response, "candidates", None
        ):
            # Defensive: avoid infinite loop
            if verbose:
                print(
                    f"No function calls or candidates on iteration {iteration}, stopping."
                )
            break

    else:
        # Loop exhausted without final text response
        print(
            f"Reached max iterations ({max_iterations}) without a final text response."
        )


def extract_text_parts(candidate):
    out = []
    for p in candidate.content or []:
        if hasattr(p, "text") and p.text:
            out.append(p.text)
    return "".join(out)


if __name__ == "__main__":
    main()
