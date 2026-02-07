"""Basic class definition example."""


class CoffeeOrder:
    """Represents a coffee order with a size and beverage."""

    def __init__(self, size: str, drink: str) -> None:
        self.size = size
        self.drink = drink

    def summary(self) -> str:
        """Return a human-friendly summary of the order."""
        return f"{self.size.title()} {self.drink.title()}"


if __name__ == "__main__":
    order = CoffeeOrder("large", "latte")
    print(order.summary())
