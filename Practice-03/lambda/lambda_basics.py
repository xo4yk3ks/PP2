"""Basic lambda examples."""


if __name__ == "__main__":
    # Simple lambda to square a number
    square_number = lambda value: value ** 2
    print(f"Square of 6: {square_number(6)}")

    # Lambda with multiple parameters
    format_coordinates = lambda x, y: f"({x}, {y})"
    print(f"Coordinates: {format_coordinates(3, 7)}")
