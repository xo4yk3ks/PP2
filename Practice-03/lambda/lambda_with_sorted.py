"""Use lambda with sorted to order complex data."""


if __name__ == "__main__":
    students = [
        {"name": "Maya", "score": 91},
        {"name": "Leo", "score": 84},
        {"name": "Sara", "score": 96},
    ]
    # Sort students by score in descending order
    sorted_students = sorted(students, key=lambda student: student["score"], reverse=True)
    print("Sorted students by score:")
    for student in sorted_students:
        print(f"{student['name']}: {student['score']}")
