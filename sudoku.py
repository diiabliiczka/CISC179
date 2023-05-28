import tkinter as tk
from tkinter import messagebox
import numpy as np


class SudokuGUI:
    def __init__(self, puzzle):
        self.grid_size = 9
        self.empty_cell = 0
        self.puzzle = puzzle
        self.window = tk.Tk()
        self.window.title("Sudoku")
        self.create_grid()
        self.solve_button = tk.Button(self.window, text="Solve", command=self.solve_puzzle)
        self.solve_button.grid(row=self.grid_size, columnspan=self.grid_size)

    def create_grid(self):
        self.entry_grid = []
        cell_font = ("Arial", 16)  # Set the desired font for the numbers

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell_value = self.puzzle[i][j]
                entry = tk.Entry(self.window, width=2, justify="center", font=cell_font)
                entry.insert(tk.END, str(cell_value) if cell_value != self.empty_cell else "")
                entry.grid(row=i, column=j, padx=1, pady=1)
                entry.config(validate="key", validatecommand=(entry.register(self.validate_input), "%P"))
                self.entry_grid.append(entry)

                # Calculate the region number (0 to 8) for the current cell
                region_num = (i // 3) * 3 + (j // 3)

                # Alternate between purple and pink for each region
                if region_num % 2 == 0:
                    entry.config(bg="lavender")
                else:
                    entry.config(bg="pink")

    def validate_input(self, new_value):
        if new_value == "":
            return True  # Allow empty input
        try:
            int_value = int(new_value)
            if 0 <= int_value <= 9:
                if all(entry.get() != "" for entry in self.entry_grid):  # Check if all inputs are filled
                    messagebox.showinfo("Congratulations", "You Did It!")
                return True
            return False
        except ValueError:
            return False

    def solve_puzzle(self):
        solved = self.solve_sudoku(self.puzzle)
        if solved:
            self.update_grid()
            tk.messagebox.showinfo("Success", "Puzzle solved successfully!")
        else:
            tk.messagebox.showinfo("Error", "Failed to solve the puzzle.")

    def solve_sudoku(self, grid):
        empty_cell = find_empty_cell(grid)
        if empty_cell is None:
            return True

        row, col = empty_cell

        for num in range(1, 10):
            if is_safe(grid, row, col, num):
                grid[row][col] = num

                if self.solve_sudoku(grid):
                    return True

                grid[row][col] = 0

        return False
    def update_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                entry = self.entry_grid[i * self.grid_size + j]
                cell_value = self.puzzle[i][j]
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(cell_value) if cell_value != self.empty_cell else "")


def used_in_row(grid, row, num):
    return num in grid[row]


def used_in_col(grid, col, num):
    return num in grid[:, col]


def used_in_box(grid, start_row, start_col, num):
    box = grid[start_row: start_row + 3, start_col: start_col + 3]
    return num in box


def is_safe(grid, row, col, num):
    return (
        not used_in_row(grid, row, num)
        and not used_in_col(grid, col, num)
        and not used_in_box(grid, row - row % 3, col - col % 3, num)
    )


def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

def load_puzzle(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            puzzle = []
            for line in lines:
                row = [int(char) for char in line.strip().split()]
                puzzle.append(row)
            return np.array(puzzle)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except ValueError:
        print(f"Error: Invalid puzzle data in file '{file_path}'.")
        return None


def write_puzzle(file_path, puzzle):
    try:
        with open(file_path, "w") as file:
            for row in puzzle:
                line = " ".join(str(num) for num in row)
                file.write(line + "\n")
        print(f"Puzzle successfully written to {file_path}")
    except IOError:
        print(f"Error: Failed to write puzzle to {file_path}")


# Example usage
puzzle = [
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

write_puzzle("puzzle.txt", puzzle)

if __name__ == "__main__":
    puzzle = load_puzzle("puzzle.txt")
    if puzzle is not None:
        gui = SudokuGUI(puzzle)
        gui.window.mainloop()