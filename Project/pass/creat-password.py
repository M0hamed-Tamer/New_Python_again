import random
import string
import json
import hashlib
import os
from datetime import datetime
from getpass import getpass
from cryptography.fernet import Fernet
import base64

# ====== Colors ======
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ====== Files ======
import os

# Get current project folder (where the script is)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Files will be created inside the same folder as the script
PASSWORD_FILE = os.path.join(BASE_DIR, "passwords.enc")
MASTER_FILE = os.path.join(BASE_DIR, "master.hash")

# ====== Encryption Helpers ======
def derive_key(password):
    """Generate a Fernet key from the master password."""
    hashed = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(token, key):
    f = Fernet(key)
    return f.decrypt(token).decode()

# ====== Master Password Functions ======
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def setup_master_password():
    if not os.path.exists(MASTER_FILE):
        print(f"{YELLOW}No master password found. Let's create one!{RESET}")
        while True:
            pwd1 = getpass("Enter new master password: ")
            pwd2 = getpass("Confirm master password: ")
            if pwd1 == pwd2 and pwd1.strip() != "":
                with open(MASTER_FILE, "w") as file:
                    file.write(hash_password(pwd1))
                print(f"{GREEN}Master password set successfully!{RESET}")
                return pwd1
            else:
                print(f"{RED}Passwords do not match or empty. Try again.{RESET}")

def verify_master_password():
    if not os.path.exists(MASTER_FILE):
        return setup_master_password()
    with open(MASTER_FILE, "r") as file:
        saved_hash = file.read().strip()
    for _ in range(3):
        pwd = getpass("Enter master password: ")
        if hash_password(pwd) == saved_hash:
            print(f"{GREEN}Access granted!{RESET}\n")
            return pwd
        else:
            print(f"{RED}Incorrect password!{RESET}")
    print(f"{RED}Too many failed attempts. Exiting...{RESET}")
    exit()

# ====== Password Manager Functions ======
def load_data(key):
    if not os.path.exists(PASSWORD_FILE):
        return []
    with open(PASSWORD_FILE, "rb") as file:
        encrypted = file.read()
    try:
        decrypted = decrypt_data(encrypted, key)
        return json.loads(decrypted)
    except:
        print(f"{RED}Failed to decrypt data. Wrong password or corrupted file.{RESET}")
        exit()

def save_data(data, key):
    json_data = json.dumps(data, indent=4)
    encrypted = encrypt_data(json_data, key)
    with open(PASSWORD_FILE, "wb") as file:
        file.write(encrypted)

def generate_strong_password(length=20):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def add_password(data):
    account_name = input(f"{YELLOW}Enter program / website / account name: {RESET}")
    strong_password = generate_strong_password()
    entry = {
        "account_name": account_name,
        "password": strong_password,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data.append(entry)
    print(f"\n{GREEN}{BOLD}Password generated and saved successfully!{RESET}")
    print(f"{BLUE}Account: {RESET}{account_name}")
    print(f"{BLUE}Password: {RESET}{strong_password}")
    print(f"{BLUE}Date: {RESET}{entry['time']}\n")

def view_all_passwords(data):
    if not data:
        print(f"{RED}No saved passwords found.{RESET}")
        return
    print(f"{BOLD}{BLUE}--- All Saved Passwords ---{RESET}")
    for entry in data:
        print(f"{YELLOW}Account:{RESET} {entry['account_name']}")
        print(f"{YELLOW}Password:{RESET} {entry['password']}")
        print(f"{YELLOW}Date:{RESET} {entry['time']}\n")

def search_password(data):
    keyword = input(f"{YELLOW}Enter account name to search: {RESET}").lower()
    found = False
    for entry in data:
        if keyword in entry['account_name'].lower():
            print(f"{GREEN}Found:{RESET}")
            print(f"{YELLOW}Account:{RESET} {entry['account_name']}")
            print(f"{YELLOW}Password:{RESET} {entry['password']}")
            print(f"{YELLOW}Date:{RESET} {entry['time']}\n")
            found = True
    if not found:
        print(f"{RED}No matching account found.{RESET}")

# ====== Main ======
if __name__ == "__main__":
    master_pwd = verify_master_password()
    key = derive_key(master_pwd)
    data = load_data(key)

    while True:
        print(f"""{BOLD}{BLUE}
--- Password Manager ---
1. Add new password
2. View all passwords
3. Search for a password
4. Exit
{RESET}""")
        choice = input(f"{YELLOW}Choose an option (1-4): {RESET}")
        
        if choice == "1":
            add_password(data)
            save_data(data, key)
        elif choice == "2":
            view_all_passwords(data)
        elif choice == "3":
            search_password(data)
        elif choice == "4":
            save_data(data, key)
            print(f"{GREEN}Goodbye!{RESET}")
            break
        else:
            print(f"{RED}Invalid option, try again.{RESET}")
