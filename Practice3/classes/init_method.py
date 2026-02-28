# init_method.py
# Demonstrates __init__ constructor

class Car:
    def __init__(self, brand, model):
        # Initializes object attributes
        self.brand = brand
        self.model = model

    def display_info(self):
        print(f"Car: {self.brand} {self.model}")

if __name__ == "__main__":
    car = Car("Toyota", "Corolla")
    car.display_info()
