import inspect
import re
import sys
import subprocess

from add_line_numbers import add_line_numbers
from fizzbuzz import fizzbuzz
from verify import verify, semi
from prompt import prompt


def replace_range_in_code(
    code: str, line_start: int, line_end: int, replacement_text: str
) -> str:
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
    """
    code = """1. print("hello world!")
2. print("hello Diana!")
3. print("hello Joel!")
"""
    verify(
        replace_range_in_code(
            code,
            line_start=2,
            line_end=2,
            replacement_text="""# Hi Nitsan!!!
# Hello Chat!""",
        ),
        options=semi,
    )


def replace_prompt(code: str, task: str) -> str:
    code_with_line_numbers = add_line_numbers(code)
    return f"""task:
{task}
<original-code-with-line-numbers>
{code_with_line_numbers}
</original-code-with-line-numbers>
format: format your response as described in the <format> section.
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
</tools>
"""


def prompt_ai_to_replace(code: str, task: str) -> str:
    return prompt(replace_prompt(code, task))


def test_agent_response_to_prompt():
    """
    <thinking-first>
    To switch lines 2 and 4, I need to replace the content of line 2 with the content of line 4 and vice versa. The line numbers are 1-based, and the replacement should keep the formatting consistent.
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
    pattern = re.compile(r"<replace>\n(\d+)-(\d+)\n(.*?)\n</replace>", re.DOTALL)

    for match in pattern.finditer(response):
        start_line = int(match.group(1))
        end_line = int(match.group(2))
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
"""
    verify(
        format_replacements(parse_replacements(response)),
        options=semi,
    )


def ai_replace(code: str, task: str) -> str:
    ai_response = prompt_ai_to_replace(code, task)
    replacements = parse_replacements(ai_response)
    for replace in replacements[::-1]:
        code = replace_range_in_code(code, *replace)
    return code, ai_response, replacements


# note how the rename is incomplete / incorrect
# the intention is valuable, but the execution is incorrect
def test_ai_replaces():
    """
    def fizzbuzz(number: int) -> str:
        x = lambda d, w: number % d == 0 and w or ""
        x = lambda d, w: n % d == 0 and w or ""
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

    with open(file, "w") as f:
        f.write(code)


def read_comments(file):
    with open(file) as f:
        return "\n".join([l for l in f.read().splitlines() if "# " in l])


def test_replace_in_file(temp_fizzbuzz_copy):
    """
    # Lambda function to check divisibility and return the corresponding word
    # Testing FizzBuzz for the first 15 numbers and verifying the output
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
    # TODO:
    # - Add more test cases for the fizzbuzz function
    # - Refactor fizzbuzz to be more optimized
    # - Add type annotations where missing
    # - Write documentation for existing functions
    # - Implement edge cases for fizzbuzz
    """
    cmd = f"python replace.py {temp_fizzbuzz_copy} 'add a todo list as a multi-line comment'"

    subprocess.run(cmd, shell=True)

    verify(
        read_comments(temp_fizzbuzz_copy),
        options=semi,
    )
