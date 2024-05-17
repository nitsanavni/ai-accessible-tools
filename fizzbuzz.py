def fizzbuzz(n: int) -> str:
    x = lambda d, w: n % d == 0 and w or ""
    a = x(3, "Fizz")
    b = x(5, "Buzz")

    return a + b or str(n)
