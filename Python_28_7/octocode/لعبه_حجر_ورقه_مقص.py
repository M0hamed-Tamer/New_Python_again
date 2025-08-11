# بسم الله الرحمن الرحيم
import random
print ("Welcome to the Rock, Paper, Scissors game:")

helps = input ("Press Enter to continue or type (Help): ").capitalize()
# 🗒️🪨 ✂️/
if helps == "Help":
    print("""            ************  RULES ************
            1) You choose and the computer chooses
            2) Rock smashes Scissors ->> Rock  Win 
            3) Scissors cut Paper ->> Scissors  Win
            4) Paper covers Rock ->> Paper  Win\n""")
    choice_computer = random.randrange(1,3) 
    choice = input ("Enter your choice (Rock, Paper, Scissors): ").capitalize()
    if choice == "Rock" or "Paper" or " Scissors":


        
    else:
        print("Invalid choice , Please run the program again and choose rock, paper, scissors.")

else :
    choice = input ("Enter your choice (Rock, Paper, Scissors)").capitalize()
    if choice == "Rock" or "Paper" or " Scissors":

        print ("asdf")
    else:
        print("Invalid choice , Please run the program again and choose rock, paper, scissors.")