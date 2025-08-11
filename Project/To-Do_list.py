
class TerminalColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK='\033[30m'
    WHITE = '\033[37m'
import os
Taskes = []
print(f"{TerminalColors.HEADER}======= welcome to the To-Do List App!======{TerminalColors.RESET}")

while True:
    try:
        
        print(f"""
Choose an option:{TerminalColors.UNDERLINE}
1. Add Task
2. View Tasks
3. Delete Task
4. Exit{TerminalColors.RESET}""")
        choice = int(input("Enter Your Choice (1-4): "))
        if choice == 1 :
            task_add =  input("Enter the task: ")
            Taskes.append(task_add)
            print("Task Added!\n")
            continue
        elif choice ==2 :
            for i in Taskes :
                print (i)
            continue
        elif choice == 3 :
            break
        else:
            print("Goodbye!")
            break
    except ValueError:
        print("Please Enter the Number.")
        continue
