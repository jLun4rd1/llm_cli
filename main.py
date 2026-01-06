import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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

    for _ in range(10):
        response = client.models.generate_content(
            model=model,
            contents=messages,
            # If disobeying happens, set the 'temperature' argument of GenerateContentConfig to 0
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            ),
        )
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if not response.usage_metadata:
            raise RuntimeError("No 'usage_metadata' property in response. Can't access token count")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        function_results = []
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)

                if not function_call_result.parts:
                    raise Exception("Missing 'parts' list in types.Content object")
                if not function_call_result.parts[0].function_response:
                    raise Exception("Missing 'function_response' property")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Missing called function response")

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_results.append(function_call_result.parts[0])

        else:
            print(f"Response:\n{response.text}")
            break

        messages.append(types.Content(role="user", parts=function_results))

        if _ == 9:
           print("Maximum number of iterations reached")
           sys.exit(1)


if __name__ == "__main__":
    main()
