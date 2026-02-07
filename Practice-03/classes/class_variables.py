"""Example of class variables shared across instances."""


class DeliveryTracker:
    """Track delivery status and total deliveries."""

    total_deliveries = 0

    def __init__(self, destination: str) -> None:
        self.destination = destination
        DeliveryTracker.total_deliveries += 1

    def status(self) -> str:
        """Return the delivery status message."""
        return f"Delivery to {self.destination} in progress."


if __name__ == "__main__":
    first_delivery = DeliveryTracker("Main Street")
    second_delivery = DeliveryTracker("Oak Avenue")
    print(first_delivery.status())
    print(second_delivery.status())
    print(f"Total deliveries: {DeliveryTracker.total_deliveries}")
