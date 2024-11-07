import tkinter as tk
from tkinter import messagebox

board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        
        
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(root, width=2, font=("Arial", 18), justify="center")
                entry.grid(row=i, column=j, padx=5, pady=5)
                if board[i][j] != 0:
                    entry.insert(0, board[i][j])
                    entry.config(state="disabled")
                self.entries[i][j] = entry

        
        solve_button = tk.Button(root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=4, pady=20)

    def get_board(self):
        
        current_board = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.entries[i][j].get()
                if value.isdigit():
                    row.append(int(value))
                else:
                    row.append(0)
            current_board.append(row)
        return current_board

    def set_board(self, solution):
        
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, solution[i][j])

    def solve(self):
        
        board = self.get_board()
        if self.solve_sudoku(board):
            self.set_board(board)
            messagebox.showinfo("Sudoku Solver", "Sudoku solved successfully!")
        else:
            messagebox.showerror("Sudoku Solver", "No solution exists for this Sudoku.")

    def is_valid(self, board, row, col, num):
        
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def solve_sudoku(self, board):
       
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve_sudoku(board):
                                return True
                            board[row][col] = 0
                    return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
