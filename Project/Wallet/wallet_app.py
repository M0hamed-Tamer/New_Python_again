# wallet.py
import json
import os
import getpass
import hashlib
from datetime import datetime

# ====== Colors ======
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ====== File paths ======
BALANCE_FILE = "wallet.json"
TRANSACTIONS_FILE = "transactions.json"
PASSWORD_FILE = "password.txt"

# ====== Helper Functions ======
# دالة لتشفير كلمة المرور (Hashing)
def hash_password(password):
    # نستخدم خوارزمية SHA-256 للتشفير
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
def load_balance():
    if not os.path.exists(BALANCE_FILE):
        return 0.0
    with open(BALANCE_FILE, "r") as f:
        data = json.load(f)
        return data.get("balance", 0.0)

def save_balance(balance):
    with open(BALANCE_FILE, "w") as f:
        json.dump({"balance": balance}, f)

def load_transactions():
    if not os.path.exists(TRANSACTIONS_FILE):
        return []
    with open(TRANSACTIONS_FILE, "r") as f:
        return json.load(f)

def save_transactions(transactions):
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump(transactions, f, indent=4)

def add_transaction(type_, amount, description):
    transactions = load_transactions()
    transactions.append({
        "type": type_,
        "amount": amount,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_transactions(transactions)

def check_password():
    # 1. التحقق من وجود ملف كلمة المرور
    if not os.path.exists(PASSWORD_FILE):
        # هذه هي حالة "الإعداد لأول مرة"
        print(YELLOW + "First time setup: Create a password" + RESET)
        while True:
            # 2. إدخال كلمة المرور وتأكيدها بشكل مخفي
            p1 = getpass.getpass("Enter new password: ")
            p2 = getpass.getpass("Confirm password: ")
            
            # 3. التأكد من تطابق كلمتي المرور وأنهما ليستا فارغتين
            if p1 == p2 and p1.strip():
                # 4. حفظ كلمة المرور المشفرة في الملف
                with open(PASSWORD_FILE, "w") as f:
                    f.write(hash_password(p1))
                print(GREEN + "Password saved successfully!" + RESET)
                break # الخروج من الحلقة لأن العملية نجحت
            else:
                print(RED + "Passwords do not match or empty. Try again." + RESET)
    else:
        # هذه هي حالة "التحقق من كلمة المرور"
        # 5. قراءة كلمة المرور المشفرة من الملف
        stored_hash = open(PASSWORD_FILE).read().strip()
        
        # 6. إعطاء المستخدم 3 محاولات
        for _ in range(3):
            pwd = getpass.getpass("Enter password: ")
            # 7. تشفير الكلمة المدخلة ومقارنتها بالكلمة المحفوظة
            if hash_password(pwd) == stored_hash:
                print(GREEN + "Access granted!" + RESET)
                return True # تم التحقق بنجاح
            else:
                print(RED + "Wrong password!" + RESET)
        
        # 8. في حالة فشل كل المحاولات
        print(RED + "Too many failed attempts. Exiting." + RESET)
        exit() # إغلاق البرنامج

# ====== Main Program ======
def main():
    print(BOLD + BLUE + "=== Simple Wallet ===" + RESET)
    check_password()

    balance = load_balance()

    while True:
        print("\n" + BOLD + "Choose an option:" + RESET)
        print(f"{GREEN}1) Add Money{RESET}")
        print(f"{RED}2) Spend Money{RESET}")
        print(f"{YELLOW}3) Show Balance{RESET}")
        print(f"{BLUE}4) Show Transactions{RESET}")
        print(f"5) Exit{RESET}")

        choice = input("Your choice: ").strip()

        if choice == "1":
            try:
                amount = float(input("Enter amount to add: "))
                if amount > 0:
                    source = input("Where did you get the money from? ").strip()
                    balance += amount
                    save_balance(balance)
                    add_transaction("ADD", amount, source)
                    print(GREEN + f"Added {amount:.2f} ({source}). New balance: {balance:.2f}" + RESET)
                else:
                    print(RED + "Amount must be positive!" + RESET)
            except ValueError:
                print(RED + "Invalid number!" + RESET)

        elif choice == "2":
            try:
                amount = float(input("Enter amount to spend: "))
                if amount > 0 and amount <= balance:
                    item = input("What did you buy? ").strip()
                    balance -= amount
                    save_balance(balance)
                    add_transaction("SPEND", amount, item)
                    print(RED + f"Spent {amount:.2f} ({item}). New balance: {balance:.2f}" + RESET)
                else:
                    print(RED + "Invalid amount or insufficient balance!" + RESET)
            except ValueError:
                print(RED + "Invalid number!" + RESET)

        elif choice == "3":
            print(YELLOW + f"Current balance: {balance:.2f}" + RESET)

        elif choice == "4":
            transactions = load_transactions()
            if not transactions:
                print(RED + "No transactions yet." + RESET)
            else:
                print(BOLD + BLUE + "\n=== Transactions ===" + RESET)
                for t in transactions:
                    color = GREEN if t["type"] == "ADD" else RED
                    print(color + f"{t['date']} | {t['type']} | {t['amount']:.2f} | {t['description']}" + RESET)

        elif choice == "5":
            print(BLUE + "Goodbye!" + RESET)
            break

        else:
            print(RED + "Invalid choice!" + RESET)

if __name__ == "__main__":
    main()
