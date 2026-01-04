import os
import argparse
from dotenv import load_dotenv
from google import genai

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
    return parser.parse_args()

def main():
    client = get_client()
    args = get_args_from_parser()
    response = client.models.generate_content(
        model=model,
        contents=args.user_prompt
    )
    if not response.usage_metadata:
        raise RuntimeError("No 'usage_metadata' property in response. Can't access token count")

    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
