import random
choice_computer = random.randrange(1,4) 

Paper ="🗒️"
Scissors="✂️"
Rock="🪨 "

if choice_computer == 1 :
    choice_computer = Paper
elif choice_computer == 2 :
    choice_computer = Scissors
else :
    choice_computer = Rock

print (choice_computer)