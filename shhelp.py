import platform
import os
import json
import sys

from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("CLI_KEY_OPENAI")
)

SYSTEM_PROMPT = f""" 
You are an expert in command-line operations. 

1. You must generate command-line that can run on {platform.system()} .
2. Do not include any additional output—only the scripts.
3. If a task requires a file, include the script to create the file with its content.
4. The output must be a json, the command must on a variable called comands, it must be an array, because may be
necessary to run multiple commands.

### Example 1:
**Input:** list all docker instances  
**Output:** 
{{
"commands": [
    "docker ps",
  ]
}}

### Example 2:
**Input:** create a new directory named Projects and a file called README.md inside it with the content "Project Documentation".
**Output:** mkdir Projects :: echo "Project Documentation" > Projects/README.md
{{
"commands": [
    "mkdir Projects",
    "echo "Project Documentation" > Projects/README.md"
  ]
}}

### Example 3:
**Input:** find all .txt files in the home directory and concatenate their contents into a file called all_texts.txt  
**Output:**
{{
"commands": [
    "find ~ -name "*.txt" -exec cat { {} } \; >",
  ]
}}
"""


def send_message_to_openai_chat_completions(model, message):
    completion = client.chat.completions.create(
        response_format={"type": "json_object"},
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ],
    )
    result = completion.choices[0].message.content
    return result


def get_commands(input_string):
    try:
        commands = json.loads(input_string)
        return commands["commands"]
    except:
        print("Unable to Parse Commands")
        return []


def ask_user_if_want_to_execute_sh_command_and_then_execute(command):
    response = input(f"Do you want to execute \n{command} ? \n(y/n):")
    print("\n")
    if response.lower() == 'y':
        import subprocess
        print(f"running {command} \n")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")


def process_chatbot_interaction():
    while True:
        user_input = input("Enter your message for the AI: \n")

        if user_input == "exit":
            sys.exit()

        response_from_ai = send_message_to_openai_chat_completions("gpt-3.5-turbo", user_input)
        commands = get_commands(response_from_ai)

        if len(commands) > 1:
            print(f"IA wants to execute: {commands} \n")

        for command in commands:
            if command:
                ask_user_if_want_to_execute_sh_command_and_then_execute(command)
            else:
                print("No command found in AI response.")


process_chatbot_interaction()
