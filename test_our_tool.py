from approvaltests import verify, Options
from approvaltests.inline.inline_options import InlineOptions
import openai
from filecache import filecache

semi = Options().inline(InlineOptions.semi_automatic())


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


@filecache
def prompt(the_prompt: str, sample=0) -> str:
    return (
        openai.chat.completions.create(
            model="gpt-4o", messages=[{"role": "user", "content": the_prompt}]
        )
        .choices[0]
        .message.content
    )


def test_prompt():
    """
    Thought:
    The user is initiating a knock-knock joke, and I should respond appropriately to continue the interaction.

    Answer:
    Who's there?
    """
    a_prompt = """format: format your response as described in the <format> section, but don't include the <format> tags.
<format>
Thought:
{think first, you thoughts here}
Answer:
{your answer here}
</format>
<query>
knock knock
</query>"""
    verify(prompt(a_prompt), options=semi)


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


def agent_replace_prompt(code: str, task: str) -> str:
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
end line number is exclusive
</constraints>
</replace-tool>
</tools>
"""


def agent_replace(code: str, task: str) -> str:
    return prompt(agent_replace_prompt(code, task))


def test_agent_uses_replace():
    """
    <thinking-first>
    To switch lines 2 and 4 in the provided code, simply place the content of line 4 where line 2 is and the content of line 2 where line 4 is. This maintains the order specified in the task.
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
    verify(agent_replace(code, task), options=semi)
