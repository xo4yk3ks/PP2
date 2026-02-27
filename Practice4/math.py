
"""Math and random operations"""

import math
import random


def circle_area(radius):
    return math.pi * radius ** 2


def random_numbers(count, start=0, end=100):
    return [random.randint(start, end) for _ in range(count)]


def factorial(n):
    return math.factorial(n)


if __name__ == "__main__":
    print("Area:", circle_area(5))
    print("Random numbers:", random_numbers(5))
    print("Factorial:", factorial(6))
