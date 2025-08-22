# name = input ('Enter names separated by a comma .. :').split(', ')
# print (type(name))
# print(name)
# print(len(name))
# ===============================================================
import random

print("Welcome to 'Whose Wallet?'")
print("You will give me a list of names, and I will pick a person to pay!")

# Step 1: أخذ الأسماء وفصلها
names = input("If you're ready, enter the names separated by a comma: ").split(',')

# Step 2: إزالة الفراغات من كل اسم
names = [name.strip() for name in names if name.strip()]
# تنضّف قائمة الأسماء بإزالة:

# أي فراغات في بداية أو نهاية كل اسم.

# أي أسماء فاضية (زي لما المستخدم يكتب ,, أو , ,).

# Step 3: اختيار عشوائي
if names:
    chosen = random.choice(names)
    print(f"Please ask '{chosen}' to take their wallet out. Dinner is on them 😄.")
else:
    print("You didn't enter any names.")
