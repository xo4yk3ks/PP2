# args_kwargs.py
# Demonstrates *args and **kwargs usage

def print_args(*args):
    # Prints all positional arguments
    for arg in args:
        print("Arg:", arg)

def print_kwargs(**kwargs):
    # Prints all keyword arguments
    for key, value in kwargs.items():
        print(f"{key} = {value}")

if __name__ == "__main__":
    print_args(1, 2, 3)
    print_kwargs(name="Alice", age=25)
