from verify import semi, verify


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
