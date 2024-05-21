import inspect
import re
import sys
import subprocess
import os

from add_line_numbers import add_line_numbers
from fizzbuzz import fizzbuzz
from verify import verify, semi
from prompt import prompt


def replace_range_in_code(
    code: str, line_start: int, line_end: int, replacement_text: str
) -> str:
    if line_start == -1:
        return "\n".join([code, replacement_text])
    lines = code.split("\n")
    lines[line_start - 1 : line_end - 1] = [replacement_text]
    return "\n".join(lines)


def test_replace():
    """
    1. print("hello world!")
    # Hi Nitsan!!!
    # Hello Chat!
    2. print("hello Diana!")
    3. print("hello Joel!")

    # This is the last line now
    """
    code = """1. print("hello world!")
2. print("hello Diana!")
3. print("hello Joel!")
"""
    code = replace_range_in_code(
        code,
        line_start=2,
        line_end=2,
        replacement_text="""# Hi Nitsan!!!
# Hello Chat!""",
    )
    code = replace_range_in_code(code, -1, -1, "# This is the last line now")
    verify(
        code,
        options=semi,
    )


def replace_prompt(code: str, task: str) -> str:
    code_with_line_numbers = add_line_numbers(code)
    return f"""task:
{task}
<original-code-with-line-numbers>
{code_with_line_numbers}
</original-code-with-line-numbers>
format:
- format your response as described in the <format> section.
- for multiple replacements, include multiple <replace> tags.
<format>
<thinking-first>
{{think first, your thoughts here}}
</thinking-first>
<response>
{{your response here}}
</response>
</format>
<tools>
<replace-tool>
<example-1>
<replace>
17-23
def myfunction():
    return 1
</replace>
<replace>
27-27
# Do the thing
</replace>
</example-1>
<example-2>
<replace>
-1
# This is the last line now
</replace>
</example-2>
<constraints>
do not repeat line numbers
end line number is exclusive, to replace a single line, use e.g. 17-18
</constraints>
</replace-tool>
<example-responses>
<example-response-1>
<thinking>was asked to add a comment, a comment would be good before line 3</thinking>
<response>
<replace>
3-3
# This is a comment
</replace>
</response>
</example-response-1>
</example-responses>
</tools>
"""


def prompt_ai_to_replace(code: str, task: str) -> str:
    return prompt(replace_prompt(code, task))


def test_agent_response_to_prompt():
    """
    <thinking-first>
    To switch lines 2 and 4, I need to replace the content of line 2 with line 4, and vice versa. Thus, I will update each of these lines accordingly.
    </thinking-first>
    <response>
    <replace>
    2-3
    print(4)
    </replace>
    <replace>
    4-5
    print(2)
    </replace>
    </response>
    """
    code = """print(1)
print(2)
print(3)
print(4)
print(5)
"""
    task = "switch 2 4"
    verify(prompt_ai_to_replace(code, task), options=semi)


def parse_replacements(response: str):
    replacements = []
    pattern = re.compile(r"<replace>\n(-?\d+)(?:-(\d+))?\n(.*?)\n</replace>", re.DOTALL)

    for match in pattern.finditer(response):
        start_line = int(match.group(1))
        end_line = int(match.group(2)) if match.group(2) is not None else start_line
        replacement_code = match.group(3)
        replacements.append((start_line, end_line, replacement_code))

    return replacements


def format_replacements(replacements):
    return "\n".join(
        [f"<replace>\n{s}-{e}\n{r}\n</replace>" for s, e, r in replacements]
    )


def test_parse_replacements():
    """
    <replace>
    2-3
    print(4)
    print(7)
    </replace>
    <replace>
    4-5
    print(2)
    </replace>
    <replace>
    -1--1
    # This is the last line now
    </replace>
    """
    response = """<replace>
2-3
print(4)
print(7)
</replace>
<replace>
4-5
print(2)
</replace>
<replace>
-1
# This is the last line now
</replace>
"""
    verify(
        format_replacements(parse_replacements(response)),
        options=semi,
    )


def ai_replace(code: str, task: str):
    ai_response = prompt_ai_to_replace(code, task)
    replacements = parse_replacements(ai_response)
    for replace in replacements[::-1]:
        code = replace_range_in_code(code, *replace)
    return code, ai_response, replacements


# note how the rename is incomplete / incorrect
# the intention is valuable, but the execution is incorrect
def test_ai_replaces():
    """
    def fizzbuzz(n: int) -> str:
        check_divisibility = lambda d, w: n % d == 0 and w or ""
        a = x(3, "Fizz")
        b = x(5, "Buzz")

        return a + b or str(n)
    """
    fizzbuzz_code = inspect.getsource(fizzbuzz)
    task = "!just! rename **one** symbol"
    code, response, replacements = ai_replace(code=fizzbuzz_code, task=task)
    verify(code, options=semi)


def replace(file: str, task: str):
    with open(file) as f:
        code = f.read()

    code, response, replacements = ai_replace(code, task)

    if "DEBUG" in os.environ:
        print("response", response)

    with open(file, "w") as f:
        f.write(code)

    return response, replacements


def read_comments(file):
    with open(file) as f:
        return "\n".join(
            ["comments:"] + [l for l in f.read().splitlines() if "# " in l]
        )


def test_replace_in_file(temp_fizzbuzz_copy):
    """
    comments:
    # Lambda function to check divisibility and return corresponding word
    # Test the FizzBuzz function for numbers 1 to 15 and compare with the expected output
    """
    replace(file=temp_fizzbuzz_copy, task="add exactly two comments")

    verify(
        read_comments(temp_fizzbuzz_copy),
        options=semi,
    )


if __name__ == "__main__":
    file = sys.argv[1]
    task = " ".join(sys.argv[2:])
    replace(file, task)


def test_from_cli(temp_fizzbuzz_copy):
    """
    from verify import verify, semi

    # TODO:
    # 1. Add more test cases to cover edge cases.
    # 2. Improve the fizzbuzz function to handle larger inputs efficiently.
    # 3. Use more descriptive variable names in the fizzbuzz function.
    # 4. Ensure that verify method and options from verify module are correctly implemented.
    def fizzbuzz(n: int) -> str:
        x = lambda d, w: n % d == 0 and w or ""
        a = x(3, "Fizz")
        b = x(5, "Buzz")

        return a + b or str(n)
    """

    task = "add a todo list as a comment"
    run_self = "python replace.py"
    cmd = f"{run_self} {temp_fizzbuzz_copy} '{task}'"

    subprocess.run(cmd, shell=True, stdout=None, env=os.environ.copy() | {"DEBUG": "1"})

    verify(
        "\n".join(
            [l for l in open(temp_fizzbuzz_copy).read().splitlines() if '"""' not in l][
                :13
            ]
        ),
        options=semi,
    )
