# basic_functions.py
# Demonstrates how to define and call basic functions

def greet_user(name):
    # Prints a greeting message
    print(f"Hello, {name}!")

def add_numbers(num1, num2):
    # Returns the sum of two numbers
    return num1 + num2

if __name__ == "__main__":
    greet_user("Alice")
    result = add_numbers(5, 3)
    print("Sum:", result)
