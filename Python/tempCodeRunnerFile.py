import os , json 
BALANCE_FILE = "file.json"
def load_balance():
    if not os.path.exists(BALANCE_FILE):
        return 0.0
    with open(BALANCE_FILE, "r") as f:
        data = json.load(f)
        return data.get("balance", 0.0)
    

print(load_balance())