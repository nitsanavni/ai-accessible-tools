from verify import verify, semi


def fizzbuzz(n: int) -> str:
    x = lambda d, w: n % d == 0 and w or ""
    a = x(3, "Fizz")
    b = x(5, "Buzz")

    return a + b or str(n)


def test_fizzbuzz():
    """
    1
    2
    Fizz
    4
    Buzz
    Fizz
    7
    8
    Fizz
    Buzz
    11
    Fizz
    13
    14
    FizzBuzz
    """
    verify("\n".join([fizzbuzz(n) for n in range(1, 16)]), options=semi)
