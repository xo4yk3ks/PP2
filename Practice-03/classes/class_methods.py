"""Example of class methods for alternative constructors."""


class Student:
    """Represents a student and their grade."""

    def __init__(self, name: str, grade: int) -> None:
        self.name = name
        self.grade = grade

    @classmethod
    def from_percentage(cls, name: str, percentage: float) -> "Student":
        """Create a student from a percentage score."""
        grade = round(percentage)
        return cls(name, grade)


if __name__ == "__main__":
    student = Student.from_percentage("Noah", 88.6)
    print(f"Student: {student.name}, Grade: {student.grade}")
