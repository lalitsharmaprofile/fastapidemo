def add(fname: str | list, lname: str = None):
    # fname.
    fname.capitalize()
    return fname + " " + lname

first_name = "None"
last_name = "Sharma"

print(add(first_name, last_name))