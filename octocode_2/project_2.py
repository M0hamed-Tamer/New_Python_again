import os
def clear():
    os.system("cls")
class User:
    def __init__(self, first_name, last_name, email, password,status="inactive"):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.status =status
    def display(self):
        clear()
        print(f"First Name: {self.first_name} ")
        print(f"Last Name: {self.last_name} ")
        print(f"Email: {self.email} ")
        print(f"Status: {self.status}")
        print("=========================")


def user_in():
    clear()
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter the email: ")
    password = input("Enter the password: ")
    print("User Added Successfully !")
    return User(first_name, last_name, email, password)


def main():
    clear()
    users = []
    while True:
        print("""\nWelcome To User Management

Choose an Action:

1. Add New User
2. Display All Users
3. Exit
""")

        choice = int(input("Enter Your Choice: "))

        if choice == 1:
            user = user_in()
            users.append(user)
        elif choice == 2:
            for user in users:
                user.display()
        elif choice == 3:
            print("Exiting.........")
            break
        else:
            print("Invalid choice. Please try again.")


main()


