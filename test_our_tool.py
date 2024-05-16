from approvaltests import verify, Options
from approvaltests.inline.inline_options import InlineOptions


def replace_range_in_code(
    code: str, line_start: int, line_end: int, replacement_text: str
) -> str:
    # Split the code into a list of lines
    lines = code.split('\n')
    
    # Replace the specified range of lines with the replacement text
    lines[line_start - 1:line_end] = [replacement_text]
    
    # Join the lines back into a single string
    return '\n'.join(lines)


def test_replace():
    """
    1. print("hello world!")
    # Hi Nitsan!!!
    3. print("hello Joel!")
    """
    code = """1. print("hello world!")
2. print("hello Diana!")
3. print("hello Joel!")
"""
    verify(
        replace_range_in_code(
            code, line_start=2, line_end=2, replacement_text="# Hi Nitsan!!!"
        ),
        options=Options().inline(InlineOptions.semi_automatic()),
    )
