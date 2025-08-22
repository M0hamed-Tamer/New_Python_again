import time
import os
from tabulate import tabulate
import pandas as pd

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

Memberships = []

class User:
    def __init__(self, first_name, last_name, membership, status):
        self.FirstName = first_name
        self.LastName = last_name
        self.Membership = membership
        self.Status = status

    def display(self):
        print(f""" First Name: {self.FirstName}
 Last Name: {self.LastName}
 Membership ID: {self.Membership}
 Membership Status: {self.Status}
_________________________________\n""")

def search():
    clear()
    print("""Search by:

1 - Membership ID
2 - First Name 
3 - Membership Status 
                        """)
    search_choice = input("Enter Your Choice: ")
    found = False

    if search_choice == "1":
        ID = input("Enter The Membership ID To Search: ")
        for member in Memberships:
            if member.Membership == ID:
                member.display()
                found = True
        if not found:
            print("Member not found.")
    elif search_choice == "2":
        first_name = input("Enter The First Name To Search: ")
        for member in Memberships:
            if member.FirstName.lower() == first_name.lower():
                member.display()
                found = True
        if not found:
            print("Member not found.")
    elif search_choice == "3":
        status = input("Enter The Membership Status To Search: ")
        clear()
        time.sleep(2)
        for member in Memberships:
            if member.Status.lower() == status.lower():
                member.display()
                found = True
        if not found:
            print("Member not found.")
    else:
        print("Invalid search choice.")
    input("Press Enter to Exit....")

def initialize_file():
    if not os.path.exists("members.xlsx"):
        df = pd.DataFrame(columns=["First Name", "Last Name", "Membership ID", "Membership Status"])
        df.to_excel("members.xlsx", index=False)

def save_to_file(user):
    df = pd.read_excel("members.xlsx")
    new_row = {"First Name": user.FirstName, "Last Name": user.LastName, "Membership ID": user.Membership, "Membership Status": user.Status}
    df = df.append(new_row, ignore_index=True)
    df.to_excel("members.xlsx", index=False)

def update_file():
    data = [{"First Name": member.FirstName, "Last Name": member.LastName, "Membership ID": member.Membership, "Membership Status": member.Status} for member in Memberships]
    df = pd.DataFrame(data)
    df.to_excel("members.xlsx", index=False)

def add_member():
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    while True:
        membership = input("Enter Membership ID: ")
        if any(x.Membership == membership for x in Memberships):
            time.sleep(2)
            print(f"'{membership}' already exists, please choose a different ID")
            time.sleep(5)
        else:
            break

    status = input("Enter Membership Status (active) or press Enter to default to inactive: ").strip()
    if not status:
        status = "inactive"

    print("Member added successfully!")
    time.sleep(3)

    new_user = User(first_name, last_name, membership, status)
    save_to_file(new_user)
    return new_user

def delete_member():
    membership = input("Enter the Membership ID of the member to delete: ")
    global Memberships
    new_memberships = [member for member in Memberships if member.Membership != membership]
    if len(new_memberships) == len(Memberships):
        print("Member not found.")
        time.sleep(2)
    else:
        Memberships = new_memberships
        update_file()
        print("Member deleted successfully!")
        time.sleep(2)

def display_file():
    clear()
    try:
        df = pd.read_excel("members.xlsx")
        print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))
    except FileNotFoundError:
        print("The members.xlsx file does not exist.")
    input("Press Enter to Exit....")

def main():
    initialize_file()

    while True:
        clear()
        print("""Welcome To Gym Membership Management

Choose an Action:
1 - Add new member
2 - Display all members
3 - Search for a member
4 - Display members from file
5 - Delete a member
6 - Exit
        """)
        try:
            choice = int(input("Enter Your Choice: "))
            if choice == 1:
                clear()
                Memberships.append(add_member())
            elif choice == 2:
                clear()
                if Memberships:
                    data = [[member.FirstName, member.LastName, member.Membership, member.Status] for member in Memberships]
                    print(tabulate(data, headers=["First Name", "Last Name", "Membership ID", "Membership Status"], tablefmt="grid"))
                    input("Press Enter to Exit....")
                else:
                    print('No members to display.')
                    time.sleep(3)
            elif choice == 3:
                search() if Memberships else print("No members to search.")
                time.sleep(3)
            elif choice == 4:
                display_file()
            elif choice == 5:
                delete_member() if Memberships else print("No members to delete.")
            elif choice == 6:
                break
            else:
                print("Invalid choice. Please try again.")
                time.sleep(3)
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
