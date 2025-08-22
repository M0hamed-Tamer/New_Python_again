import os , json 
BALANCE_FILE = "file.json"
def load_balance():
    try:
        if not os.path.exists(BALANCE_FILE):
            return 0.0
        with open(BALANCE_FILE, "r") as f:
            data = json.load(f)
            return data.get("balance", 0.0)
    except json.decoder.JSONDecodeError:
        i = {"balance" : 0.0}
        with open(BALANCE_FILE,"w") as file:
            json.dump(i,file,indent=4)
        return 0.0

print(load_balance())   