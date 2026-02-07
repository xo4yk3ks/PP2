"""Use lambda with filter to select data."""


if __name__ == "__main__":
    order_totals = [49.99, 120.00, 15.75, 200.50, 89.10]
    # Keep only orders above 50
    high_value_orders = list(filter(lambda total: total > 50, order_totals))
    print(f"All orders: {order_totals}")
    print(f"High-value orders: {high_value_orders}")
