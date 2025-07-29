import time
import os
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
    input("Enter To Exit....")
def add_member():
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    while True:
        membership = input("Enter Membership ID: ")
        for x in Memberships:
            if x.Membership == membership:
                time.sleep(2)
                print(f"' {membership} ' already exists, please choose a different ID")
                time.sleep(5)
                Memberships.remove(membership)

                continue



        status = input("Enter Membership Status (active) or click Enter: ").strip()

        print("Member added successfully!")
        time.sleep(3)


        if not status :
            status ="inactive"
        return User(first_name, last_name, membership, status)
def main():
    while True:
        clear()
        print("""Welcome To Gym Membership Management

Choose an Action:
1 - Add new member
2 - Display all members
3 - Search for a member
4 - Exit
        """)
        try:
            choice = int(input("Enter Your Choice: "))
            if choice == 1:
                clear()
                Memberships.append(add_member())
            elif choice == 2:
                clear()
                if Memberships:
                    print("Displaying all members...\n")
                    time.sleep(3)
                    for member in Memberships:
                        member.display()
                    input("Please Enter To Exit....")
                else:
                    print('Try again....')
                    time.sleep(3)
            elif choice == 3:
                search() if Memberships else print("Try again....")
                time.sleep(3)
            elif choice == 4:
                break
            else:
                print("Invalid choice. Please try again.")
                time.sleep(3)
        except ValueError:
            print("Invalid input. Please enter a number.")
if __name__ == "__main__":
    main()