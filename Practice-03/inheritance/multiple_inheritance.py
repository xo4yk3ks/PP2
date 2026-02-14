# multiple_inheritance.py
# Demonstrates multiple inheritance

class Flyable:
    def fly(self):
        print("Flying")

class Swimmable:
    def swim(self):
        print("Swimming")

class Duck(Flyable, Swimmable):
    pass

if __name__ == "__main__":
    duck = Duck()
    duck.fly()
    duck.swim()
