"""Example of multiple inheritance."""


class Flyer:
    """Provides flying capability."""

    def fly(self) -> str:
        """Return a flying message."""
        return "Flying through the sky!"


class Swimmer:
    """Provides swimming capability."""

    def swim(self) -> str:
        """Return a swimming message."""
        return "Swimming in the water!"


class Duck(Flyer, Swimmer):
    """Duck can both fly and swim."""

    def sound(self) -> str:
        """Return the duck's sound."""
        return "Quack!"


if __name__ == "__main__":
    duck = Duck()
    print(duck.sound())
    print(duck.fly())
    print(duck.swim())
