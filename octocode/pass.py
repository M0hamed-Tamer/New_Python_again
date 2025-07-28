
import random
import string

def generate_password(length=18):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

while True:
    user_input = input("Type 'y' to generate a new password or 'n' to exit: ").strip().lower()
    if user_input == 'y':
        print("New password: ", generate_password())
    elif user_input == 'n':
        print("Exiting")
        break
    else:
        print("Invalid input, please try again")
