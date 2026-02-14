# class_methods.py
# Demonstrates instance and class methods

class MathUtils:
    @classmethod
    def add(cls, a, b):
        # Returns sum of two numbers
        return a + b

if __name__ == "__main__":
    print("Sum:", MathUtils.add(10, 5))
