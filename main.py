import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
model = os.environ.get("GEMINI_MODEL")
if not any([api_key, model]):
    raise RuntimeError("Couldn't load API credentials from .env")

def get_client():
    return genai.Client(api_key=api_key)

def get_args_from_parser():
    parser = argparse.ArgumentParser(description="LLM CLI")
    parser.add_argument("user_prompt", type=str, help="Your input. Use it with wisdom")
    parser.add_argument("--verbose", action="store_true", help="Enables verbose output, such as tokens metadata")
    return parser.parse_args()

def main():
    client = get_client()
    args = get_args_from_parser()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model=model,
        contents=messages,
        # If disobeying happens, set the 'temperature' argument of GenerateContentConfig to 0
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
    if not response.usage_metadata:
        raise RuntimeError("No 'usage_metadata' property in response. Can't access token count")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
