# super_function.py
# Demonstrates use of super()

class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

if __name__ == "__main__":
    dog = Dog("Buddy", "Labrador")
    print(dog.name, dog.breed)
