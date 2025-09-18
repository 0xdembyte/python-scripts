import string
from random import randint, choice
from enum import Enum

# Values that are going to be set later by the user (Note: including symbols and digits is on by default and can't be set by the user as it isn't implemented)
password_include_symbols = True
password_include_digits  = True
password_length          = 32

class StringType(Enum):
    UPPERCASE = "uppercase"
    LOWERCASE = "lowercase"
    DIGIT     = "digit"
    SYMBOL    = "symbol"

def get_random_character(ascii_text: str):
    return ascii_text[randint(0, len(ascii_text) - 1)]

def generate_character(type : StringType):
    match type.value:
        case StringType.UPPERCASE.value:
            return get_random_character(string.ascii_uppercase)
        case StringType.LOWERCASE.value:
            return get_random_character(string.ascii_lowercase)
        case StringType.DIGIT.value:
            return get_random_character(string.digits)
        case StringType.SYMBOL.value:
            return get_random_character(string.punctuation)

def get_random_string_type():
    return choice(list(StringType))

def generate_random_password():
    allowed_types = [StringType.UPPERCASE, StringType.LOWERCASE]
    if password_include_digits:
        allowed_types.append(StringType.DIGIT)
    if password_include_symbols:
        allowed_types.append(StringType.SYMBOL)

    generated_password = "".join(generate_character(choice(allowed_types)) for _ in range(password_length))
    print(f"Generated password: {generated_password}")

def get_option(prompt_msg="Option: "):
    option = input(prompt_msg).strip().lower()
    return option

def set_password_length():
    desired_password_length = get_option("Password length: ")
    if not desired_password_length.isdigit():
        print("Unexpected input! Please enter integer values only.")
        return None
    return int(desired_password_length)


def display_as_list(display_items : list, message="Item", counter_reqd=True):
    if len(display_items) == 0:
        print("Sorry, the list is empty.")
        return False
    
    print()

    for item_index, item_value in enumerate(display_items, 1):
        if counter_reqd:
            print(f"{message} {item_index}: {item_value}")
        else:
            print(item_value)

    return True

while True:
    display_as_list(display_items=[
        "Password generator options.",
        "A) Generate a random password",
        "B) Set the maximum length of the password e.g., 32 characters.",
        "Q) Quit."
    ], message="", counter_reqd=False)

    selected_option = get_option()
    match selected_option:
        case "a":
            generate_random_password()
        case "b":
            new_length = set_password_length()
            if new_length:
                password_length = new_length
        case "q":
            break
        case _:
            print("Invalid option, please try again.")
