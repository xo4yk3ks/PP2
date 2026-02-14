# return_values.py
# Demonstrates returning multiple values

def calculate(a, b):
    # Returns sum and product of two numbers
    return a + b, a * b

if __name__ == "__main__":
    sum_result, product_result = calculate(4, 6)
    print("Sum:", sum_result)
    print("Product:", product_result)
