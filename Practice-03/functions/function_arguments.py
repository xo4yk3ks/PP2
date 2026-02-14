# function_arguments.py
# Demonstrates different types of function arguments

def describe_pet(pet_name, animal_type="dog"):
    # Prints information about a pet
    print(f"I have a {animal_type} named {pet_name}.")

if __name__ == "__main__":
    describe_pet("Buddy")
    describe_pet("Whiskers", "cat")
