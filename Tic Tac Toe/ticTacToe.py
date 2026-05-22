import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import pickle

# Initialize global variables
current_player = "X"
winner = False
buttons = []
player1_name = ""
player2_name = ""
player1_score = 0
player2_score = 0

# Load scores from file
def load_scores():
    global player1_score, player2_score
    if os.path.exists("scores.pkl"):
        with open("scores.pkl", "rb") as f:
            scores = pickle.load(f)
            player1_score = scores.get("player1", 0)
            player2_score = scores.get("player2", 0)

# Save scores to file
def save_scores():
    scores = {
        "player1": player1_score,
        "player2": player2_score
    }
    with open("scores.pkl", "wb") as f:
        pickle.dump(scores, f)

# Reset the game board
def reset_board():
    global winner, current_player
    winner = False
    current_player = "X"
    for button in buttons:
        button.config(text="", bg="SystemButtonFace")
    # No need to change scores here

# Check for winner or tie
def check_winner():
    global winner, player1_score, player2_score
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combinations:
        if (buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != ""):
            buttons[combo[0]].config(bg="green")
            buttons[combo[1]].config(bg="green")
            buttons[combo[2]].config(bg="green")
            winner = True
            if buttons[combo[0]]["text"] == player1_name:
                player1_score += 1
            else:
                player2_score += 1
            save_scores()
            messagebox.showinfo("Tic-Tac-Toe", f"Player {buttons[combo[0]]['text']} wins!")
            root.quit()
            return
    if all(button["text"] != "" for button in buttons) and not winner:
        messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
        root.quit()

# Button click handler
def button_click(index):
    global current_player, winner
    if buttons[index]["text"] == "" and not winner:
        buttons[index]["text"] = current_player
        check_winner()
        if not winner:
            toggle_player()

# Switch the current player
def toggle_player():
    global current_player
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"

# Restart the game
def restart_game():
    reset_board()
    # No need to change scores

# Create the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Ask for player names
player1_name = simpledialog.askstring("Player 1", "Enter your name:")
player2_name = simpledialog.askstring("Player 2", "Enter your name:")

# Load previous scores
load_scores()

# Display player names and scores
score_label = tk.Label(root, text=f"{player1_name}: {player1_score} | {player2_name}: {player2_score}", font=("Helvetica", 12))
score_label.grid(row=0, column=0, columnspan=3, pady=10)

# Create buttons
for i in range(9):
    button = tk.Button(root, text="", font=("Helvetica", 24), width=5, height=2, command=lambda i=i: button_click(i))
    button.grid(row=1 + i // 3, column=i % 3, padx=5, pady=5)
    buttons.append(button)

# Restart button
restart_button = tk.Button(root, text="Restart", font=("Helvetica", 12), command=restart_game)
restart_button.grid(row=4, column=0, columnspan=3, pady=10)

# Main loop
root.mainloop()