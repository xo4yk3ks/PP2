"""Example of method overriding in inheritance."""


class Person:
    """Represents a person with a first and last name."""

    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    def introduction(self) -> str:
        """Return a basic introduction."""
        return f"Hi, I'm {self.first_name} {self.last_name}."


class Teacher(Person):
    """Teacher overrides the introduction to add a subject."""

    def __init__(self, first_name: str, last_name: str, subject: str) -> None:
        super().__init__(first_name, last_name)
        self.subject = subject

    def introduction(self) -> str:
        """Return an introduction that includes the subject taught."""
        base_intro = super().introduction()
        return f"{base_intro} I teach {self.subject}."


if __name__ == "__main__":
    teacher = Teacher("Ravi", "Sharma", "Mathematics")
    print(teacher.introduction())
