import tkinter as tk
from tkinter import messagebox
import random
from collections import deque

# Initialize board and constants
board = [" " for _ in range(9)]
player = "X"
computer = "O"

# GUI setup
window = tk.Tk()
window.title("Stylish Tic-Tac-Toe")
window.geometry("400x700")
window.configure(bg="#f2e1f2")

selected_algorithm = tk.StringVar(value="BFS")

# Function definitions
def reset_board():
    global board
    board = [" " for _ in range(9)]
    print_board()
    enable_buttons()  # Enable buttons after reset

def enable_buttons():
    for button in buttons:
        button.config(state="normal")  # Enable all buttons

def disable_buttons():
    for button in buttons:
        button.config(state="disabled")  # Disable all buttons

def print_board():
    for i in range(9):
        buttons[i].config(text=board[i], bg="#f4f4f9", fg="#5d3fd3", state="normal")

def check_winner(player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    return any(all(board[pos] == player for pos in cond) for cond in win_conditions)

def check_draw():
    return " " not in board

def on_button_click(index):
    if board[index] == " ":
        board[index] = player
        print_board()
        if check_winner(player):
            messagebox.showinfo("Game Over", "You win!")
            disable_buttons()  # Disable buttons after the game ends
            return
        elif check_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_buttons()  # Disable buttons after the game ends
            return
        else:
            computer_move()

# BFS Algorithm Implementation
def bfs_move():
    queue = deque([(board, None)])  # Each item is (board_state, move_index)
    while queue:
        current_board = queue.popleft()[0]
        for i in range(9):
            if current_board[i] == " ":
                new_board = current_board[:]
                new_board[i] = computer
                if check_winner_in_board(new_board, computer):
                    return i  # Winning move found
                queue.append((new_board, i))
    return random.choice([i for i in range(9) if board[i] == " "])

# DFS Algorithm Implementation
def dfs_move():
    def dfs(board_state):
        for i in range(9):
            if board_state[i] == " ":
                new_board = board_state[:]
                new_board[i] = computer
                if check_winner_in_board(new_board, computer):
                    return i  # Winning move found
                result = dfs(new_board)
                if result is not None:
                    return result
        return None

    return dfs(board) or random.choice([i for i in range(9) if board[i] == " "])

# Uniform Cost Search
def uniform_cost_move():
    return bfs_move()

# IDDFS Algorithm Implementation
def iddfs_move():
    depth = 0
    while True:
        best_move = dls_move(depth)
        if best_move is not None:
            return best_move
        depth += 1

def dls_move(limit):
    for i in range(9):
        if board[i] == " ":
            board[i] = computer
            score = dfs(board, 0, limit, False)
            board[i] = " "
            if score == 1:  # winning move found
                return i
    return None

def dfs(board_state, depth, limit, is_maximizing):
    if check_winner_in_board(board_state, computer):
        return 1
    if check_winner_in_board(board_state, player):
        return -1
    if check_draw() or depth == limit:
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board_state[i] == " ":
                board_state[i] = computer
                score = dfs(board_state, depth + 1, limit, False)
                board_state[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board_state[i] == " ":
                board_state[i] = player
                score = dfs(board_state, depth + 1, limit, True)
                board_state[i] = " "
                best_score = min(score, best_score)
        return best_score

# Helper function to check winner in a hypothetical board
def check_winner_in_board(board_state, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    return any(all(board_state[pos] == player for pos in cond) for cond in win_conditions)

# Main computer move function
def computer_move():
    if check_winner(player) or check_draw():  # Check if game is over
        return

    algorithm = selected_algorithm.get()
    if algorithm == "BFS":
        move = bfs_move()
    elif algorithm == "DFS":
        move = dfs_move()
    elif algorithm == "Uniform Cost":
        move = uniform_cost_move()
    elif algorithm == "IDDFS":
        move = iddfs_move()
    else:
        move = random.choice([i for i in range(9) if board[i] == " "])

    if move is not None and board[move] == " ":
        board[move] = computer
        print_board()
        if check_winner(computer):
            messagebox.showinfo("Game Over", "Computer wins!")
            disable_buttons()  # Disable buttons after the game ends
        elif check_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_buttons()  # Disable buttons after the game ends

# UI Layout
header = tk.Label(window, text="New Game", font=("Arial", 24, "bold"), bg="#f2e1f2", fg="#5d3fd3")
header.pack(pady=10)

# Create a frame for board buttons
board_frame = tk.Frame(window, bg="#f2e1f2")
board_frame.pack(pady=10)

buttons = []
for i in range(9):
    button = tk.Button(board_frame, text=" ", font=("Arial", 20), width=5, height=2,
                       bg="#f4f4f9", fg="#5d3fd3", activebackground="#c9a6e8",
                       command=lambda i=i: on_button_click(i))
    button.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(button)

# Control Buttons
control_frame = tk.Frame(window, bg="#f2e1f2")
control_frame.pack(pady=20)

play_button = tk.Button(control_frame, text="Play", font=("Arial", 14), bg="#8e5fe8", fg="white",
                        width=10, height=2, command=reset_board)
play_button.grid(row=0, column=0, padx=5)

# Algorithm Selection Dropdown
algorithm_label = tk.Label(window, text="Select Algorithm:", font=("Arial", 12), bg="#f2e1f2", fg="#5d3fd3")
algorithm_label.pack()
algorithm_menu = tk.OptionMenu(window, selected_algorithm, "BFS", "DFS", "Uniform Cost", "IDDFS")
algorithm_menu.config(font=("Arial", 12), bg="#f4f4f9", fg="#5d3fd3")
algorithm_menu.pack(pady=5)

# Run the GUI
window.mainloop()
