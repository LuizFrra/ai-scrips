import argparse
import os

from openai import OpenAI

# SETUP ARGUMENT PARSER
parser = argparse.ArgumentParser(description="Helps you coding a file")
parser.add_argument("f", type=str, help="Path of to file where the AI should code")
parser.add_argument(
    "-m", type=str, help="Model to use to execute the task", default="3t", nargs="?"
)
args = parser.parse_args()


# END SETUP ARGUMENT PARSER


# HELP FUNCTIONS
def file_exists(filepath):
    return os.path.isfile(filepath)


def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()


# END HELP FUNCTIONS

models_mapping = {
    "3t": "gpt-3.5-turbo",
    "4t": "gpt-4-turbo",
    "4o": "gpt-4o",
}

client = OpenAI(
    api_key=os.environ.get("CLI_KEY_OPENAI")
)

SYSTEM_PROMPT = """
You are a software expert tasked with modifying programming code snippets based on specific instructions embedded within the code. 

### Instructions:
1. User provides a code snippet.
2. Check if the code contains the string `{{CODE_%INSTRUCTION%}}`.
3. If the string is not present, return the code as is.
4. If the string is present, replace `{{CODE_%INSTRUCTION%}}` with the correct code based on the `%INSTRUCTION%` and the context.
5. Respond with just the modified code, do not include your thoughts or anything else.

### Example 1:

**Input:**
```python
def calculate_sum(a, b):
    return {{CODE_ADD_NUMBERS}}
```

**Output:**
```python
def calculate_sum(a, b):
    return a + b
```

### Example 2:

**Input:**
```python
def greet(name):
    return "Hello, {{CODE_USER_NAME}}!"
```

**Output:**
```python
def greet(name):
    return f"Hello, {name}!"
```

### Example 3:

**Input:**
```javascript
function multiply(a, b) {
    return {{CODE_MULTIPLY_NUMBERS}};
}
```

**Output:**
```javascript
function multiply(a, b) {
    return a * b;
}
```

### Example 4:

**Input:**
```java
public int findMax(int[] nums) {
    int max = {{CODE_INITIALIZE_MAX}};
    for (int num : nums) {
        if (num > max) {
            max = num;
        }
    }
    return max;
}
```

**Output:**
```java
public int findMax(int[] nums) {
    int max = Integer.MIN_VALUE;
    for (int num : nums) {
        if (num > max) {
            max = num;
        }
    }
    return max;
}
"""

if not file_exists(args.f):
    print(f"File '{args.f}' does not exist.")
    raise "The given file does not exist"

data = read_file(args.f)

model = models_mapping[args.m]

completion = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": data
        }
    ],
)

print(completion.choices[0].message.content)
