from approvaltests import verify, Options
from approvaltests.inline.inline_options import InlineOptions


def replace_range_in_code(
    code: str, line_start: int, line_end: int, replacement_text: str
) -> str:
    code = """
print("hello world!")
# Hi Nitsan!!!
print("hello Joel!")
"""
    return code


def test_replace():
    """
    
    print("hello world!")
    # Hi Nitsan!!!
    print("hello Joel!")
    ***** DELETE ME TO APPROVE *****
    """
    code = """
print("hello world!")
print("hello Diana!")
print("hello Joel!")
"""
    verify(
        replace_range_in_code(
            code, line_start=2, line_end=2, replacement_text="# Hi Nitsan!!!"
        ),
        options=Options().inline(InlineOptions.semi_automatic()),
    )
