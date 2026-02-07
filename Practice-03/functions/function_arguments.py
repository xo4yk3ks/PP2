"""Examples of different types of function arguments."""


def format_full_name(first_name: str, last_name: str, middle_name: str = "") -> str:
    """Return a properly spaced full name with an optional middle name."""
    if middle_name:
        return f"{first_name} {middle_name} {last_name}"
    return f"{first_name} {last_name}"


def describe_book(title: str, author: str, *, published_year: int) -> str:
    """Return a formatted description using a keyword-only argument."""
    return f"{title} by {author} ({published_year})"


if __name__ == "__main__":
    # Positional arguments
    print(format_full_name("Ada", "Lovelace"))

    # Keyword arguments with a default middle name
    print(format_full_name(first_name="Alan", middle_name="Mathison", last_name="Turing"))

    # Keyword-only argument example
    print(describe_book("Clean Code", "Robert C. Martin", published_year=2008))
