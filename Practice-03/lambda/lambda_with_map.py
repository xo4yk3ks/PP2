"""Use lambda with map to transform data."""


if __name__ == "__main__":
    temperatures_c = [0, 10, 20, 30]
    # Convert each Celsius temperature to Fahrenheit
    temperatures_f = list(map(lambda c: (c * 9 / 5) + 32, temperatures_c))
    print(f"Celsius: {temperatures_c}")
    print(f"Fahrenheit: {temperatures_f}")
