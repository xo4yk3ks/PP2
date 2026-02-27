
"""Iterator and generator exercises"""

class CountUpTo:
    """Simple iterator that counts from 1 to max"""
    def __init__(self, max_value):
        self.max = max_value
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.max:
            value = self.current
            self.current += 1
            return value
        raise StopIteration


def even_numbers(limit):
    """Generator that yields even numbers up to limit"""
    for i in range(0, limit + 1):
        if i % 2 == 0:
            yield i


def fibonacci(n):
    """Generator that yields first n Fibonacci numbers"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


if __name__ == "__main__":
    counter = CountUpTo(5)
    print(list(counter))

    print(list(even_numbers(10)))
    print(list(fibonacci(10)))
