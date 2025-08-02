
import string
import random
import os

def clear():
    """Clear The Terminal"""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def generate_password(num_letters, num_numbers, num_symbols):
    num_password = random.choices(string.digits, k=num_numbers)
    let_password = random.choices(string.ascii_letters, k=num_letters)
    sym_password = random.choices(string.punctuation, k=num_symbols)
    password = num_password + let_password + sym_password
    random.shuffle(password)
    return ''.join(password)

def main():
    try:
        clear()
        saved_passwords = []
        print("Welcome to the Password Generator!")

        choose_length = int(input("Enter the total number of characters in the password: "))
        num_letters = int(input("Enter the number of letters in the password: "))
        num_numbers = int(input("Enter the number of numbers in the password: "))
        num_symbols = int(input("Enter the number of symbols in the password: "))

        total = num_letters + num_numbers + num_symbols

        if choose_length == total and num_letters >= 0 and num_numbers >= 0 and num_symbols >= 0:
            while True:
                password = generate_password(num_letters, num_numbers, num_symbols)
                clear()
                print(f"The Password ==> {password}")
                save = input("Do you want to save your password (Y/N)? ").strip().upper()
                if save == "Y":
                    saved_passwords.append(password)
                print("Saved Passwords:")
                for idx, pwd in enumerate(saved_passwords, 1):
                    print(f"{idx}: {pwd}")
                repeat_password = input("Do you want another password? (Y/N)? ").strip().upper()
                if repeat_password != "Y":
                    clear()
                    print("#" * 50)
                    print("All Saved Passwords:")
                    for idx, pwd in enumerate(saved_passwords, 1):
                        print(f"{idx}: {pwd}")
                    print("#" * 50)
                    
                    break

        else:
            print("Invalid input. The sum of letters, numbers, and symbols doesn't match the password length.")
            
    except ValueError:
        print("Invalid input. Please enter integer values.")
        

if __name__ == "__main__":
    main()

input("Press Enter to exit...... ")