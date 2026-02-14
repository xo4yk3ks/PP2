# lambda_with_sorted.py
# Using lambda with sorted()

students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78}
]

if __name__ == "__main__":
    sorted_students = sorted(students, key=lambda student: student["grade"])
    print("Sorted by grade:", sorted_students)
