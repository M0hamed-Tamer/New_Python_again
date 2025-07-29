# import random

# print("Welcome to the Coin Guessing Game!")

# method = int(input("""Choose a method to toss the coin:
# 1. Using random.random()
# 2. Using random.randint()
# Enter your choice (1 or 2): """))

# # تحديد نتيجة العملة حسب الطريقة المختارة
# if method == 1:
#     guess = input("Enter your guess (Heads or Tails): ").lower()
#     if guess not in ["heads", "tails"]:
#         print("Invalid guess. Please enter 'Heads' or 'Tails'.")
#         exit()

#     choose_computer = random.random()
#     if choose_computer < 0.5:
#         coin_result = "heads"
#     else:
#         coin_result = "tails"

# elif method == 2:
#     guess = input("Enter your guess (Heads or Tails): ").lower()
#     if guess not in ["heads", "tails"]:
#         print("Invalid guess. Please enter 'Heads' or 'Tails'.")
#         exit()

#     choose_computer = random.randint(1, 2)
#     if choose_computer == 1:
#         coin_result = "heads"
#     else:
#         coin_result = "tails"
# else:
#     print("Invalid choice. Please select either 1 or 2.")
#     exit()

# # مقارنة النتيجة بتوقع اللاعب
# if guess == coin_result:
#     print("🎉 Win! The coin was", coin_result)
# else:
#     print("❌ Lose! The coin was", coin_result)
# ======================================================
import random

print("""Welcome to the Coin Guessing Game!
Choose a method to toss the coin:
1. Using random.random()
2. Using random.randint()
""")

choice = int(input("Enter your choice (1 or 2): "))

if choice == 1:
    random_number = random.random()
    if random_number >= 0.5:
        computer = "heads"
    else:
        computer = "tails"

elif choice == 2:
    random_number = random.randint(0, 1)
    if random_number == 0:
        computer = "heads"
    else:
        computer = "tails"

else:
    print("Invalid choice. Please select either 1 or 2.")

user_choice = input("Enter your guess (Heads or Tails): ").lower()

if user_choice == "heads":
    if user_choice == computer:
        print(f"🎉 Win! The coin was--> {computer}")
    else:
        print(f"❌ Lose! The coin was--> {computer}")

elif user_choice == "tails":
    if user_choice == computer:
        print(f"🎉 Win! The coin was--> {computer}")
    else:
        print(f"❌ Lose! The coin was--> {computer}")

else:
    print("Invalid input. Please enter 'Heads' or 'Tails'.")
