"""Basic inheritance example based on W3Schools Python Inheritance."""


class Person:
    """Represents a person with a first and last name."""

    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    def print_name(self) -> None:
        """Print the person's full name."""
        print(f"{self.first_name} {self.last_name}")


class Student(Person):
    """Student inherits from Person."""

    pass


if __name__ == "__main__":
    student = Student("John", "Doe")
    student.print_name()
