import random
print ("🎲 Welcome to the Number Guessing Game!")
computer  = random.randint(1 , 10)
tries = 0
while True:
    try:
        user = int (input("Guess a number between 1 and 10: "))
        if computer == user :
            print(f"🎉 Correct! You guessed the number in {tries} tries")
            break
        else:
            if computer < user :
                print("🔽 Too high! Try again.")
                tries += 1 
                continue
            else:
                print ("🔼 Too Low! Try again.")
                tries += 1 
                continue
    except ValueError :
        print("No, Enter the number!..............")  
          

