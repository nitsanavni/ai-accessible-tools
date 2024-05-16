from approvaltests import verify, Options

def replace_range_in_code(
    code: str, line_start: int, line_end: int, replacement_text: str
) -> str:
    pass


def test_replace():
    code = """
print("hello world!")
print("hello Diana!")
print("hello Joel!")
"""
    verify (replace_range_in_code(code, line_start=2, line_end=2, replacement_text="# Hi Nitsan!!!") 
