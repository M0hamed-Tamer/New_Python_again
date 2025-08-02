import os
import time
import json

def clear():
    """مسح الشاشة حسب نظام التشغيل"""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def load_tasks(file_path):
    """تحميل المهام من ملف JSON"""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

def save_tasks(file_path, tasks):
    """حفظ المهام في ملف JSON"""
    with open(file_path, 'w') as file:
        json.dump(tasks, file, indent=4)

print("             Welcome To The Build To-Do List Application with Python             \n")

Message = """
1 - Add tasks to a list
2 - Mark task as complete
3 - View tasks
4 - Quit 
"""

Tasks = load_tasks("tasks.json")

def Add_Task():
   
    time.sleep(2)
    clear()
    Task = input("Enter task: ")
    Task_info = {"Task": Task, "Complete": False}
    Tasks.append(Task_info)
    
    print("Task added to the list successfully.")
    time.sleep(2)
    save_tasks("tasks.json", Tasks)

def Mark_Task():
    
    time.sleep(2)
    clear()
    if not Tasks:
        print("No tasks to mark as complete.")
        return
    
    View_Tasks()
    try:
        time.sleep(1)
        task_index = int(input("Enter the number of the task to mark as complete: ")) - 1
        if 0 <= task_index < len(Tasks):
            Tasks[task_index]["Complete"] = True
            time.sleep(1)
            print("Task marked as complete.")
            time.sleep(2)
            save_tasks("tasks.json", Tasks)
        else:
            time.sleep(2)
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")
        time.sleep(2)

def View_Tasks():
    
    time.sleep(2)
    clear()
    if not Tasks:
        print("No tasks in the list.")
        return
    time.sleep(1)
    print("Tasks List:")
    for index, task in enumerate(Tasks, start=1):
        status = "Complete" if task["Complete"] else "Incomplete"
        print(f"{index}. {task['Task']} - {status}")
    print() 
    time.sleep(4)
    

while True:
    clear()
    print(Message)
    Choice = input("Enter Your Choice: ")
    if Choice == "1":
        Add_Task()
    elif Choice == "2":
        Mark_Task()
    elif Choice == "3":
        View_Tasks()
        time.sleep(2)
    elif Choice == "4":
        print("Exiting the application.")
        save_tasks("tasks.json", Tasks)
        break
    else:
        print("Invalid choice, Please enter a number between 1 and 4.")
        time.sleep(2)
