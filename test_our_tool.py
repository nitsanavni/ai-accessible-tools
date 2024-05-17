from approvaltests import verify, Options
from approvaltests.inline.inline_options import InlineOptions

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


def agent_replace(code: str, task: str) -> str:
    return prompt(agent_replace_prompt(code, task))


def test_agent_uses_replace():
    code = """print(1)
print(2)
print(3)
print(4)
print(5)
"""
    task = "switch 2 4"
    verify(agent_replace(code, task), options=semi)
