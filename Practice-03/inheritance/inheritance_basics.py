# inheritance_basics.py
# Basic inheritance example

class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    pass

if __name__ == "__main__":
    dog = Dog()
    dog.speak()
