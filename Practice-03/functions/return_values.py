"""Examples that return values from functions."""


def convert_celsius_to_fahrenheit(celsius_temp: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius_temp * 9 / 5) + 32


def summarize_scores(scores: list[int]) -> dict[str, float]:
    """Return min, max, and average score statistics."""
    average_score = sum(scores) / len(scores)
    return {
        "min": min(scores),
        "max": max(scores),
        "average": average_score,
    }


if __name__ == "__main__":
    temperature_c = 21.5
    temperature_f = convert_celsius_to_fahrenheit(temperature_c)
    print(f"{temperature_c}°C = {temperature_f}°F")

    quiz_scores = [88, 92, 79, 93, 85]
    summary = summarize_scores(quiz_scores)
    print(f"Score summary: {summary}")
