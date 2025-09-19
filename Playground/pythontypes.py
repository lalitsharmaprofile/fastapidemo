def add(first: str, last: str = None):
    first.capitalize()
    return first + " " + last

first_name = "None"
last_name = "Sharma"

print(add(first_name, last_name))