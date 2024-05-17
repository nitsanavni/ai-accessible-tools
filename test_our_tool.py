import inspect
import re

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


def add_line_numbers(code: str) -> str:
    lines = code.split("\n")
    return "\n".join([f"{i+1}\t|{line}" for i, line in enumerate(lines)])


def test_add_line_numbers():
    """
    1	|import mymodule
    2	|
    3	|def myfunction():
    4	|    return 1
    5	|
    """
    code = """import mymodule

def myfunction():
    return 1
"""
    verify(add_line_numbers(code), options=semi)


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
    I need to switch lines 2 and 4 in the original code. This means I'll place the content of line 4 where line 2 was and vice versa. The lines currently are:
    1. `print(1)`
    2. `print(2)`
    3. `print(3)`
    4. `print(4)`
    5. `print(5)`

    After switching, the new order will be:
    1. `print(1)`
    2. `print(4)`
    3. `print(3)`
    4. `print(2)`
    5. `print(5)`

    I will now proceed to write the necessary replacements.
    </thinking-first>

    <response>
    <replace-tool>
    <replace>
    2-3
    print(4)
    </replace>
    <replace>
    4-5
    print(2)
    </replace>
    </replace-tool>
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
    """
    Parses a response string and returns a list of tuples representing replacements.
    Each tuple contains the start line, end line, and the replacement code.

    Args:
    response (str): The input string containing replacement directives.

    Returns:
    List[Tuple[int, int, str]]: A list of tuples with replacements.
    """
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


# note how the rename is incomplete
# the intention is valuable, but the execution is incorrect
def test_ai_replaces():
    """
    <thinking-first>
    In the given code, we need to rename exactly one symbol. Essentially, renaming a symbol means changing its identifier (variable name, function name, etc.) to something else. The symbols in the code are: `fizzbuzz`, `n`, `x`, `d`, `w`, `a`, `b`, and their usages.

    To keep the change meaningful yet minimal, I'll choose to rename the symbol `a` since it appears twice (declaration and usage), making it a straightforward but effective modification.
    </thinking-first>

    <response>
    <replace-tool>
    <replace>
    3-4
        fizz_result = x(3, "Fizz")
        b = x(5, "Buzz")
    </replace>
    <replace>
    6-7
        return fizz_result + b or str(n)
    </replace>
    </replace-tool>
    </response>

    def fizzbuzz(n: int) -> str:
        x = lambda d, w: n % d == 0 and w or ""
        fizz_result = x(3, "Fizz")
        b = x(5, "Buzz")
        b = x(5, "Buzz")

        return fizz_result + b or str(n)


    <replace>
    3-4
        fizz_result = x(3, "Fizz")
        b = x(5, "Buzz")
    </replace>
    <replace>
    6-7
        return fizz_result + b or str(n)
    </replace>
    """
    fizzbuzz_code = inspect.getsource(fizzbuzz)
    task = "!just! rename **one** symbol"
    code, response, replacements = ai_replace(code=fizzbuzz_code, task=task)
    verify(f"{response}\n\n{code}\n\n{format_replacements(replacements)}", options=semi)
