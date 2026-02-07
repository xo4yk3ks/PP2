"""Examples of basic function definitions and calls."""


def greet_user(user_name: str) -> None:
    """Print a friendly greeting."""
    print(f"Hello, {user_name}!")


def calculate_rectangle_area(width: float, height: float) -> float:
    """Return the area of a rectangle."""
    return width * height


# Run examples when this file is executed directly
if __name__ == "__main__":
    greet_user("Amina")

    rectangle_width = 4.5
    rectangle_height = 2.0
    area = calculate_rectangle_area(rectangle_width, rectangle_height)
    print(f"Area: {area}")
