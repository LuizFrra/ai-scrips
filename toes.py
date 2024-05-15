import argparse
import os

from openai import OpenAI

# SETUP ARGUMENT PARSER
parser = argparse.ArgumentParser(description="Translate to Spanish")
parser.add_argument("p", type=str, help="Phrase which you want to translate", nargs="+")
parser.add_argument(
    "-m", type=str, help="Model to use to execute the task", default="3t", nargs="?"
)
args = parser.parse_args()

# END SETUP ARGUMENT PARSER

models_mapping = {
    "3t": "gpt-3.5-turbo",
    "4t": "gpt-4-turbo",
    "4o": "gpt-4o",
}

client = OpenAI(
    api_key=os.environ.get("CLI_KEY_OPENAI")
)

SYSTEM_PROMPT = """
You are a helpful assistant that specializes in translating text from any language to Spanish. Your job is to provide accurate and clear translations.
Whenever someone inputs text in any language, respond only with the Spanish translation and nothing else.
"""

model = models_mapping[args.m]

user_input: str = " ".join(args.p)

if user_input is None:
    raise "Phrase is required"

if user_input.strip() == "":
    raise "Phrase cant be empty"

completion = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_input
        }
    ],
)

print(completion.choices[0].message.content)
