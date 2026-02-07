"""Example showing how __init__ sets up instance data."""


class WorkoutSession:
    """Track a workout session with duration and activity type."""

    def __init__(self, activity: str, minutes: int) -> None:
        self.activity = activity
        self.minutes = minutes

    def calories_burned(self, calories_per_minute: int) -> int:
        """Estimate total calories burned for the session."""
        return self.minutes * calories_per_minute


if __name__ == "__main__":
    session = WorkoutSession("cycling", 45)
    print(f"Activity: {session.activity}")
    print(f"Estimated calories: {session.calories_burned(8)}")
