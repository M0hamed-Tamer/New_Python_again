import json

# لقراءه م في ملف  json
with open ("file.json","r") as file:
    i = json.load(file)
print(i)
# =========================================
# للكتابه في ملف json
data = {
    "name": "Mohamed Tamer",
    "age": 20,
    "skills": ["Python", "Cyber Security", "Linux"]
}

with open('file.json', "w") as file:
    json.dump(data, file , indent= 4)

