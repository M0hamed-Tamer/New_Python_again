# List   ----->   []  
friends = ['Mohamed ','Tamer','Fared','Ali']
print(f"The first friend on our list is  {friends [0]}, and the last friend on our list is {friends [-1]}")

for i in friends :
    if i == 'Ali':
        print (len (i))
    else:
        exit
# نفس الحاجه بتعرف مكان الحاجه الي في list ف  فكره كويسه /
print(friends.index('Tamer'))

# ==========================================================
colors = [ ]
colors.append(input('Add the firs color you like: '))
user_add = input("Do you want to add more colors? Yes,No : ").lower()
if user_add == 'yes':
    colors.append(input('Add colors you like are:'))
    print (colors)
else:
    print(colors)

# ==========================================================
class_a = ['Tom', 'Jack ','Sarah','Ben']
class_b = ['Fred','Tina','Mohamed','Tamer']

print (class_a + class_b)
print(class_a)
print(class_b)
print(type(class_a))
# # ============================================================
name = input('Enter the name: ')
if name:
    print(f'Hello, {name}')
else:
    print("You forgot to enter you name:")
# =============================================================

