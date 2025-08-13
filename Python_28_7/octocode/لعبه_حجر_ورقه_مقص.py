import random

# تعريف الرموز
Paper = "🗒️"
Scissors = "✂️"
Rock = "🪨"

# اختيار الكمبيوتر عشوائياً
choices = [Rock, Paper, Scissors]
choice_computer = random.choice(choices)

# عرض مساعدة لو المستخدم طلب
helps = input("Press Enter to continue or type (Help): ").capitalize()
if helps == "Help":
    print("""
            ************  RULES ************
            1) You choose and the computer chooses
            2) Rock smashes Scissors ->> Rock wins
            3) Scissors cut Paper ->> Scissors wins
            4) Paper covers Rock ->> Paper wins
    """)

# استقبال اختيار المستخدم
choice = input("Enter your choice (Rock, Paper, Scissors): ").capitalize()

# تحويل الاختيار إلى الرمز المناسب
if choice == "Rock":
    choice_user = Rock
elif choice == "Paper":
    choice_user = Paper
elif choice == "Scissors":
    choice_user = Scissors
else:
    print("Invalid choice, please run the program again and choose Rock, Paper, or Scissors.")
    exit()

print(f"\nYou chose: {choice_user}")
print(f"Computer chose: {choice_computer}\n")

# تحديد النتيجة
if choice_user == choice_computer:
    print("It's a tie! 🤝")
else:
    # حالات الفوز للمستخدم
    if (choice_user == Rock and choice_computer == Scissors) or \
       (choice_user == Scissors and choice_computer == Paper) or \
       (choice_user == Paper and choice_computer == Rock):
        print("You Win! 🎉")
    else:
        print("You Lose! 😢")
        