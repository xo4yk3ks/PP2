# lambda_with_map.py
# Using lambda with map()

numbers = [1, 2, 3, 4]

if __name__ == "__main__":
    squared_numbers = list(map(lambda x: x ** 2, numbers))
    print("Squared:", squared_numbers)
