# Rock Paper Scissors Game
'''
WORKFLOW OF PROJECT
1. Get user input (rock, paper, scissors)
2. Generate computer choice randomly
3. Determine the winner based on the rules of the game
4. Display the result to the user

CASES:

A. Rock
Rock - Rock: Tie
Rock - Paper: Computer wins
Rock - Scissors: User wins

B. Paper
Paper - Rock: User wins
Paper - Paper: Tie
Paper - Scissors: Computer wins

C. Scissors
Scissors - Rock: Computer wins
Scissors - Paper: User wins
Scissors - Scissors: Tie
'''

import random
item_list = ['rock', 'paper', 'scissors']
user_choice = input("Enter your choice (rock, paper, scissors): ").lower()
comp_choice = random.choice(item_list)
print(f"You chose: {user_choice}, Computer chose: {comp_choice}")
if user_choice == comp_choice:
    print("It's a tie!")
elif (user_choice == 'rock'):
    if comp_choice == 'paper':
        print("Computer wins!")
    else:
        print("You win!")

elif (user_choice == 'paper'):
    if comp_choice == 'scissors':
        print("Computer wins!")
    else:
        print("You win!")

elif (user_choice == 'scissors'):
    if comp_choice == 'paper':
        print("You win!")
    else:
        print("Computer wins!")
else:
    print("Invalid choice. Please choose rock, paper, or scissors.")
