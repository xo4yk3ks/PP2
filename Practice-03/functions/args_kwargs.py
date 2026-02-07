"""Examples using *args and **kwargs."""


def total_items(*item_counts: int) -> int:
    """Return the total count from any number of integer arguments."""
    return sum(item_counts)


def build_profile(**details: str) -> dict[str, str]:
    """Return a profile dictionary built from keyword arguments."""
    return details


if __name__ == "__main__":
    # *args example
    print(f"Total items: {total_items(2, 5, 3, 4)}")

    # **kwargs example
    user_profile = build_profile(name="Priya", role="Data Analyst", location="Nairobi")
    print(f"Profile: {user_profile}")
