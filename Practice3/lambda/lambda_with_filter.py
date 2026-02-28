# lambda_with_filter.py
# Using lambda with filter()

numbers = [1, 2, 3, 4, 5, 6]

if __name__ == "__main__":
    even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
    print("Even numbers:", even_numbers)
