"""Use super() in a subclass constructor, based on W3Schools."""


class Person:
    """Represents a person with a first and last name."""

    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    def print_name(self) -> None:
        """Print the person's full name."""
        print(f"{self.first_name} {self.last_name}")


class Student(Person):
    """Student adds a graduation year."""

    def __init__(self, first_name: str, last_name: str, graduation_year: int) -> None:
        super().__init__(first_name, last_name)
        self.graduation_year = graduation_year

    def welcome(self) -> None:
        """Print a welcome message for the student."""
        print(
            f"Welcome {self.first_name} {self.last_name} to the class of {self.graduation_year}!"
        )


if __name__ == "__main__":
    student = Student("Emma", "Nguyen", 2026)
    student.print_name()
    student.welcome()
