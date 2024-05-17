from approvaltests import verify, Options
from approvaltests.inline.inline_options import InlineOptions
import openai
from filecache import filecache

semi = Options().inline(InlineOptions.semi_automatic())


def replace_range_in_code(
    code: str, line_start: int, line_end: int, replacement_text: str
) -> str:
    lines = code.split("\n")
    lines[line_start - 1 : line_end] = [replacement_text]
    return "\n".join(lines)


def test_replace():
    """
    1. print("hello world!")
    # Hi Nitsan!!!
    # Hello Chat!
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
format: format your response as described in the <format> section.
<format>
<thinking-first>
{{think first, your thoughts here}}
</thinking-first>
<new-code>
{{your new code here}}
</new-code>
</format>
"""


def agent_replace(code: str, task: str) -> str:
    return prompt(agent_replace_prompt(code, task))


def test_agent_uses_replace():
    """
    <thinking-first>
    The task requires switching the second and fourth elements of an unspecified list. Assuming the input is a list, I will swap the elements at indices 1 and 3. This requires a simple index assignment.
    </thinking-first>
    <new-code>
    def switch_2_4(lst):
        if len(lst) >= 4:
            lst[1], lst[3] = lst[3], lst[1]
        return lst

    # Example usage
    example_list = [1, 2, 3, 4, 5]
    result = switch_2_4(example_list)
    print(result)  # Output should be [1, 4, 3, 2, 5]
    </new-code>
    ***** DELETE ME TO APPROVE *****
    """
    code = """print(1)
print(2)
print(3)
print(4)
print(5)
"""
    task = "switch 2 4"
    verify(agent_replace(code, task), options=semi)
