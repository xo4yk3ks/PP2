# class_variables.py
# Demonstrates class variables

class Counter:
    count = 0  # Class variable

    def __init__(self):
        Counter.count += 1

if __name__ == "__main__":
    c1 = Counter()
    c2 = Counter()
    print("Number of instances:", Counter.count)
