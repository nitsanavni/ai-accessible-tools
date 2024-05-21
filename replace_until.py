from verify import verify, semi
from replace import replace
from add_line_numbers import add_line_numbers
from filecache import filecache
import subprocess


def black(file: str) -> str:
    result = subprocess.run(
        ["black", file], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return_code = result.returncode
    output = result.stdout.decode("utf-8") or "no output"
    error = result.stderr.decode("utf-8") or "no error"
    return f"""
black {file}
exit code: {return_code}
stdout:
{output}
stderr:
{error}
"""


def test_black(temp_fizzbuzz_copy):
    """

    exit code: 0
    stdout:
    no output
    stderr:
    All done! ✨ 🍰 ✨
    1 file left unchanged.
    """
    verify(
        "\n".join(
            [l for l in black(file=temp_fizzbuzz_copy).splitlines() if "black" not in l]
        ),
        options=semi,
    )


def replace_until(file: str, task: str, until: callable, max_iterations=10):
    def read_file(file):
        return add_line_numbers(open(file).read())

    original_code = read_file(file)
    meta_task = (
        lambda: f"""required change: {task}
you will perform one iteration out of many, some iterations were already made
if the task is done, just respond with 'done' and do not employ a tool
original code was:
{original_code}
feedback on current code:
{until()}"""
    )
    responses = []
    file_versions = [original_code]
    done = False
    iterations = 0
    while not done:
        iterations += 1
        if iterations > max_iterations:
            break
        print(meta_task())
        # infinite loop because of caching prompt responses
        # TODO: pass in a `sample`
        response, replacements = replace(file=file, task=meta_task())
        responses.append(response)
        file_versions.append(read_file(file))
        done = "done" in response and len(replacements) == 0
        if done:
            break
    return "\n\n".join(responses) + "\n\n" + "\n\n".join(file_versions)


def test_replace_until(temp_fizzbuzz_copy):
    """
    <thinking-first>
    The task is to rename the lambda function in the provided code. The lambda function is defined and assigned to the variable `x` in line 5. To improve code readability, we will change the name of `x` to something more descriptive, such as `is_divisible_message`. This change will help clarify the purpose of the lambda function.
    
    </thinking-first>
    <response>
    <replace>
    5-6
        is_divisible_message = lambda d, w: n % d == 0 and w or ""
    </replace>
    </response>
    
    <thinking-first>
    The feedback suggests renaming the lambda function 'x' to 'is_divisible_message'. Based on the provided code, the lambda function name has been updated in its definition, but the old name 'x' is still being used when calling the function on lines 6 and 7. These need to be updated to 'is_divisible_message' to reflect the new name.
    </thinking-first>
    <response>
    <replace>
    6-8
        a = is_divisible_message(3, "Fizz")
        b = is_divisible_message(5, "Buzz")
    </replace>
    </response>
    
    <thinking-first>
    The task requires renaming the lambda function in the code provided. The lambda function is defined at line 5, and the next iteration of renaming this function is to make the name more descriptive. The previous name started with the prefix "is_" indicating a check or condition, so we should maintain consistency by preserving this kind of naming. 
    </thinking-first>
    <response>
    <replace>
    5-6
    is_divisible_by_num_msg = lambda d, w: n % d == 0 and w or ""
    </replace>
    </response>
    
    <thinking-first>
    The initial task is to rename the lambda function to "is_divisible_by_num_msg". However, in the updated code, there are a couple of issues:
    1. The lambda declaration is not correctly indented.
    2. Subsequent usage of the lambda is referring to an incorrect name `is_divisible_message`.
    
    I'll fix these issues by ensuring the lambda function is properly indented and updating its usage to the correct name.
    </thinking-first>
    <response>
    <replace>
    5-5
        is_divisible_by_num_msg = lambda d, w: n % d == 0 and w or ""
    </replace>
    <replace>
    6-7
        a = is_divisible_by_num_msg(3, "Fizz")
        b = is_divisible_by_num_msg(5, "Buzz")
    </replace>
    </response>
    
    <thinking-first>
    It looks like the task is to rename the lambda function on line 5 to `is_divisible_by_num_msg` in the `fizzbuzz` function. There are remnants of partial changes on line 6, which need to be corrected. Line 6 currently contains a misplaced assignment of `is_divisible_by_num_msg` that needs to be removed.
    
    Additionally, line 9 contains an incorrect reference to `is_divisible_message`. This should be corrected to `is_divisible_by_num_msg`.
    
    The goal is to ensure consistency in the lambda's naming and remove any extraneous code.
    </thinking-first>
    <response>
    <replace>
    6-7
        a = is_divisible_by_num_msg(3, "Fizz")
    </replace>
    <replace>
    9-9
    </replace>
    </response>
    
    <thinking-first>
    It seems there was a mistake in the feedback section of the previous changes. There are duplicates in lines 7 and 9 that should not be there. Specifically for the lambda naming, we need to correct these. We should focus on ensuring the lambda function has a consistent new name throughout the code.
    
    I will correct the lambda name in lines 7 and 9 to ensure consistency.
    </thinking-first>
    
    <response>
    <replace>
    7-8
    a = is_divisible_by_num_msg(3, "Fizz")
    b = is_divisible_by_num_msg(5, "Buzz")
    </replace>
    </response>
    
    <thinking-first>
    It appears that multiple changes have already been made to rename the lambda, but some of them were either incorrect or redundant, resulting in incomplete changes. The original lambda was supposed to be renamed to `is_divisible_by_num_msg` but there are still inconsistencies.
    
    The correct and consistent name for the lambda across the code should be maintained. Let’s fix this by keeping the correct lambda name `is_divisible_by_num_msg` wherever it should be.
    
    We need to make sure that the lambda name is consistently used in lines 4, 5, 6, 7, and 9.
    </thinking-first>
    <response>
    <replace>
    7-8
        b = is_divisible_by_num_msg(5, "Buzz")
    </replace>
    </response>
    
    <thinking-first>
    It looks like the lambda function was supposed to be renamed, but there were some redundant lines and mistakes in the existing code that created parsing errors. Specifically, there are repeating and incorrect assignments to the variable `b` on lines 8, 9, and 10, causing confusion. We need to correct these lines by ensuring the lambda function is renamed properly and the extra lines removed. 
    </thinking-first>
    <response>
    <replace>
    8-11
    </replace>
    </response>
    
    <thinking-first>
    It looks like the lambda function was supposed to be renamed, but there were some redundant lines and mistakes in the existing code that created parsing errors. Specifically, there are repeating and incorrect assignments to the variable `b` on lines 8, 9, and 10, causing confusion. We need to correct these lines by ensuring the lambda function is renamed properly and the extra lines removed. 
    </thinking-first>
    <response>
    <replace>
    8-11
    </replace>
    </response>
    
    <thinking-first>
    It looks like the lambda function was supposed to be renamed, but there were some redundant lines and mistakes in the existing code that created parsing errors. Specifically, there are repeating and incorrect assignments to the variable `b` on lines 8, 9, and 10, causing confusion. We need to correct these lines by ensuring the lambda function is renamed properly and the extra lines removed. 
    </thinking-first>
    <response>
    <replace>
    8-11
    </replace>
    </response>
    
    1	|from verify import verify, semi
    2	|
    3	|
    4	|def fizzbuzz(n: int) -> str:
    5	|    x = lambda d, w: n % d == 0 and w or ""
    6	|    a = x(3, "Fizz")
    7	|    b = x(5, "Buzz")
    8	|
    9	|    return a + b or str(n)
    10	|
    11	|
    12	|def test_fizzbuzz():
    13	|    """
    14	|    1
    15	|    2
    16	|    Fizz
    17	|    4
    18	|    Buzz
    19	|    Fizz
    20	|    7
    21	|    8
    22	|    Fizz
    23	|    Buzz
    24	|    11
    25	|    Fizz
    26	|    13
    27	|    14
    28	|    FizzBuzz
    29	|    """
    30	|    verify("\n".join([fizzbuzz(n) for n in range(1, 16)]), options=semi)
    31	|
    32	|
    33	|def test_fizzbuzz_of_1():
    34	|    assert fizzbuzz(1) == "1"
    35	|
    
    1	|from verify import verify, semi
    2	|
    3	|
    4	|def fizzbuzz(n: int) -> str:
    5	|    is_divisible_message = lambda d, w: n % d == 0 and w or ""
    6	|    a = x(3, "Fizz")
    7	|    b = x(5, "Buzz")
    8	|
    9	|    return a + b or str(n)
    10	|
    11	|
    12	|def test_fizzbuzz():
    13	|    """
    14	|    1
    15	|    2
    16	|    Fizz
    17	|    4
    18	|    Buzz
    19	|    Fizz
    20	|    7
    21	|    8
    22	|    Fizz
    23	|    Buzz
    24	|    11
    25	|    Fizz
    26	|    13
    27	|    14
    28	|    FizzBuzz
    29	|    """
    30	|    verify("\n".join([fizzbuzz(n) for n in range(1, 16)]), options=semi)
    31	|
    32	|
    33	|def test_fizzbuzz_of_1():
    34	|    assert fizzbuzz(1) == "1"
    35	|
    
    1	|from verify import verify, semi
    2	|
    3	|
    4	|def fizzbuzz(n: int) -> str:
    5	|    is_divisible_message = lambda d, w: n % d == 0 and w or ""
    6	|    a = is_divisible_message(3, "Fizz")
    7	|    b = is_divisible_message(5, "Buzz")
    8	|
    9	|    return a + b or str(n)
    10	|
    11	|
    12	|def test_fizzbuzz():
    13	|    """
    14	|    1
    15	|    2
    16	|    Fizz
    17	|    4
    18	|    Buzz
    19	|    Fizz
    20	|    7
    21	|    8
    22	|    Fizz
    23	|    Buzz
    24	|    11
    25	|    Fizz
    26	|    13
    27	|    14
    28	|    FizzBuzz
    29	|    """
    30	|    verify("\n".join([fizzbuzz(n) for n in range(1, 16)]), options=semi)
    31	|
    32	|
    33	|def test_fizzbuzz_of_1():
    34	|    assert fizzbuzz(1) == "1"
    35	|
    
    1	|from verify import verify, semi
    2	|
    3	|
    4	|def fizzbuzz(n: int) -> str:
    5	|is_divisible_by_num_msg = lambda d, w: n % d == 0 and w or ""
    6	|    a = is_divisible_message(3, "Fizz")
    7	|    b = is_divisible_message(5, "Buzz")
    8	|
    9	|    return a + b or str(n)
    10	|
    11	|
    12	|def test_fizzbuzz():
    13	|    """
    14	|    1
    15	|    2
    16	|    Fizz
    17	|    4
    18	|    Buzz
    19	|    Fizz
    20	|    7
    21	|    8
    22	|    Fizz
    23	|    Buzz
    24	|    11
    25	|    Fizz
    26	|    13
    27	|    14
    28	|    FizzBuzz
    29	|    """
    30	|    verify("\n".join([fizzbuzz(n) for n in range(1, 16)]), options=semi)
    31	|
    32	|
    33	|def test_fizzbuzz_of_1():
    34	|    assert fizzbuzz(1) == "1"
    35	|
    
    1	|from verify import verify, semi
    2	|
    3	|
    4	|def fizzbuzz(n: int) -> str:
    5	|    is_divisible_by_num_msg = lambda d, w: n % d == 0 and w or ""
    6	|is_divisible_by_num_msg = lambda d, w: n % d == 0 and w or ""
    7	|    a = is_divisible_by_num_msg(3, "Fizz")
    8	|    b = is_divisible_by_num_msg(5, "Buzz")
    9	|    b = is_divisible_message(5, "Buzz")
    10	|
    11	|    return a + b or str(n)
    12	|
    13	|
    14	|def test_fizzbuzz():
    15	|    """
    16	|    1
    17	|    2
    18	|    Fizz
    19	|    4
    20	|    Buzz
    21	|    Fizz
    22	|    7
    23	|    8
    24	|    Fizz
    25	|    Buzz
    26	|    11
    27	|    Fizz
    28	|    13
    29	|    14
    30	|    FizzBuzz
    31	|    """
    32	|    verify("\n".join([fizzbuzz(n) for n in range(1, 16)]), options=semi)
    33	|
    34	|
    35	|def test_fizzbuzz_of_1():
    36	|    assert fizzbuzz(1) == "1"
    37	|
    
    1	|from verify import verify, semi
    2	|
    3	|
    4	|def fizzbuzz(n: int) -> str:
    5	|    is_divisible_by_num_msg = lambda d, w: n % d == 0 and w or ""
    6	|    a = is_divisible_by_num_msg(3, "Fizz")
    7	|    a = is_divisible_by_num_msg(3, "Fizz")
    8	|    b = is_divisible_by_num_msg(5, "Buzz")
    9	|    b = is_divisible_message(5, "Buzz")
    10	|
    11	|    return a + b or str(n)
    12	|
    13	|
    14	|def test_fizzbuzz():
    15	|    """
    16	|    1
    17	|    2
    18	|    Fizz
    19	|    4
    20	|    Buzz
    21	|    Fizz
    22	|    7
    23	|    8
    24	|    Fizz
    25	|    Buzz
    26	|    11
    27	|    Fizz
    28	|    13
    29	|    14
    30	|    FizzBuzz
    31	|    """
    32	|    verify("\n".join([fizzbuzz(n) for n in range(1, 16)]), options=semi)
    33	|
    34	|
    35	|def test_fizzbuzz_of_1():
    36	|    assert fizzbuzz(1) == "1"
    37	|
    
    1	|from verify import verify, semi
    2	|
    3	|
    4	|def fizzbuzz(n: int) -> str:
    5	|    is_divisible_by_num_msg = lambda d, w: n % d == 0 and w or ""
    6	|    a = is_divisible_by_num_msg(3, "Fizz")
    7	|a = is_divisible_by_num_msg(3, "Fizz")
    8	|b = is_divisible_by_num_msg(5, "Buzz")
    9	|    b = is_divisible_by_num_msg(5, "Buzz")
    10	|    b = is_divisible_message(5, "Buzz")
    11	|
    12	|    return a + b or str(n)
    13	|
    14	|
    15	|def test_fizzbuzz():
    16	|    """
    17	|    1
    18	|    2
    19	|    Fizz
    20	|    4
    21	|    Buzz
    22	|    Fizz
    23	|    7
    24	|    8
    25	|    Fizz
    26	|    Buzz
    27	|    11
    28	|    Fizz
    29	|    13
    30	|    14
    31	|    FizzBuzz
    32	|    """
    33	|    verify("\n".join([fizzbuzz(n) for n in range(1, 16)]), options=semi)
    34	|
    35	|
    36	|def test_fizzbuzz_of_1():
    37	|    assert fizzbuzz(1) == "1"
    38	|
    
    1	|from verify import verify, semi
    2	|
    3	|
    4	|def fizzbuzz(n: int) -> str:
    5	|    is_divisible_by_num_msg = lambda d, w: n % d == 0 and w or ""
    6	|    a = is_divisible_by_num_msg(3, "Fizz")
    7	|    b = is_divisible_by_num_msg(5, "Buzz")
    8	|b = is_divisible_by_num_msg(5, "Buzz")
    9	|    b = is_divisible_by_num_msg(5, "Buzz")
    10	|    b = is_divisible_message(5, "Buzz")
    11	|
    12	|    return a + b or str(n)
    13	|
    14	|
    15	|def test_fizzbuzz():
    16	|    """
    17	|    1
    18	|    2
    19	|    Fizz
    20	|    4
    21	|    Buzz
    22	|    Fizz
    23	|    7
    24	|    8
    25	|    Fizz
    26	|    Buzz
    27	|    11
    28	|    Fizz
    29	|    13
    30	|    14
    31	|    FizzBuzz
    32	|    """
    33	|    verify("\n".join([fizzbuzz(n) for n in range(1, 16)]), options=semi)
    34	|
    35	|
    36	|def test_fizzbuzz_of_1():
    37	|    assert fizzbuzz(1) == "1"
    38	|
    
    1	|from verify import verify, semi
    2	|
    3	|
    4	|def fizzbuzz(n: int) -> str:
    5	|    is_divisible_by_num_msg = lambda d, w: n % d == 0 and w or ""
    6	|    a = is_divisible_by_num_msg(3, "Fizz")
    7	|    b = is_divisible_by_num_msg(5, "Buzz")
    8	|b = is_divisible_by_num_msg(5, "Buzz")
    9	|    b = is_divisible_by_num_msg(5, "Buzz")
    10	|    b = is_divisible_message(5, "Buzz")
    11	|
    12	|    return a + b or str(n)
    13	|
    14	|
    15	|def test_fizzbuzz():
    16	|    """
    17	|    1
    18	|    2
    19	|    Fizz
    20	|    4
    21	|    Buzz
    22	|    Fizz
    23	|    7
    24	|    8
    25	|    Fizz
    26	|    Buzz
    27	|    11
    28	|    Fizz
    29	|    13
    30	|    14
    31	|    FizzBuzz
    32	|    """
    33	|    verify("\n".join([fizzbuzz(n) for n in range(1, 16)]), options=semi)
    34	|
    35	|
    36	|def test_fizzbuzz_of_1():
    37	|    assert fizzbuzz(1) == "1"
    38	|
    
    1	|from verify import verify, semi
    2	|
    3	|
    4	|def fizzbuzz(n: int) -> str:
    5	|    is_divisible_by_num_msg = lambda d, w: n % d == 0 and w or ""
    6	|    a = is_divisible_by_num_msg(3, "Fizz")
    7	|    b = is_divisible_by_num_msg(5, "Buzz")
    8	|b = is_divisible_by_num_msg(5, "Buzz")
    9	|    b = is_divisible_by_num_msg(5, "Buzz")
    10	|    b = is_divisible_message(5, "Buzz")
    11	|
    12	|    return a + b or str(n)
    13	|
    14	|
    15	|def test_fizzbuzz():
    16	|    """
    17	|    1
    18	|    2
    19	|    Fizz
    20	|    4
    21	|    Buzz
    22	|    Fizz
    23	|    7
    24	|    8
    25	|    Fizz
    26	|    Buzz
    27	|    11
    28	|    Fizz
    29	|    13
    30	|    14
    31	|    FizzBuzz
    32	|    """
    33	|    verify("\n".join([fizzbuzz(n) for n in range(1, 16)]), options=semi)
    34	|
    35	|
    36	|def test_fizzbuzz_of_1():
    37	|    assert fizzbuzz(1) == "1"
    38	|
    
    1	|from verify import verify, semi
    2	|
    3	|
    4	|def fizzbuzz(n: int) -> str:
    5	|    is_divisible_by_num_msg = lambda d, w: n % d == 0 and w or ""
    6	|    a = is_divisible_by_num_msg(3, "Fizz")
    7	|    b = is_divisible_by_num_msg(5, "Buzz")
    8	|b = is_divisible_by_num_msg(5, "Buzz")
    9	|    b = is_divisible_by_num_msg(5, "Buzz")
    10	|    b = is_divisible_message(5, "Buzz")
    11	|
    12	|    return a + b or str(n)
    13	|
    14	|
    15	|def test_fizzbuzz():
    16	|    """
    17	|    1
    18	|    2
    19	|    Fizz
    20	|    4
    21	|    Buzz
    22	|    Fizz
    23	|    7
    24	|    8
    25	|    Fizz
    26	|    Buzz
    27	|    11
    28	|    Fizz
    29	|    13
    30	|    14
    31	|    FizzBuzz
    32	|    """
    33	|    verify("\n".join([fizzbuzz(n) for n in range(1, 16)]), options=semi)
    34	|
    35	|
    36	|def test_fizzbuzz_of_1():
    37	|    assert fizzbuzz(1) == "1"
    38	|
    ***** DELETE ME TO APPROVE *****
    """

    def until():
        b = black(file=temp_fizzbuzz_copy)
        print(b)
        return b

    verify(
        replace_until(
            file=temp_fizzbuzz_copy,
            task="rename the lambda",
            until=until,
        ),
        options=semi,
    )
