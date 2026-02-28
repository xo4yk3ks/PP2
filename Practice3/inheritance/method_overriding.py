# method_overriding.py
# Demonstrates method overriding

class Animal:
    def speak(self):
        print("Animal sound")

class Cat(Animal):
    def speak(self):
        print("Meow")

if __name__ == "__main__":
    cat = Cat()
    cat.speak()
