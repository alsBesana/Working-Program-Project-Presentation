#A.L. Schatz A. Besana
import tkinter as tk
from tkinter import messagebox
import random, os

base_dir = os.path.dirname(os.path.realpath(__file__)) + "\\"

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("A Simple Tic Tac Toe Game")
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.load_scores()
        self.create_board()
        self.create_scoreboard()

        # creates the menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # adds game menu
        self.game_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Game", menu=self.game_menu)
        self.game_menu.add_command(label="Reset Game", command=self.reset_game)
        self.game_menu.add_command(label="Reset Scoreboard", command=self.reset_scoreboard)
        self.game_menu.add_separator()
        self.game_menu.add_command(label="Quit", command=self.root.quit)

    def load_scores(self):
        try:
            with open(base_dir + "scores.txt", "r") as file:
                self.x_wins, self.ai_wins = map(int, file.readline().split())
        except FileNotFoundError:
            self.x_wins = 0
            self.ai_wins = 0

    def save_scores(self):
        with open(base_dir + "scores.txt", "w") as file:
            file.write(f"{self.x_wins} {self.ai_wins}")
            file.close()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text="", font=("Comic Sans", 25), width=8, height=4,
                                                command=lambda i=i, j=j: self.on_click(i, j))
                self.buttons[i][j].grid(row=i, column=j)

    def create_scoreboard(self):
        self.scoreboard_frame = tk.Frame(self.root)
        self.scoreboard_frame.grid(row=4, column=0, columnspan=3)
        tk.Label(self.scoreboard_frame, text="Scoreboard").pack()
        self.x_wins_label = tk.Label(self.scoreboard_frame, text=f"Number of Player X wins: {self.x_wins}")
        self.x_wins_label.pack()
        self.ai_wins_label = tk.Label(self.scoreboard_frame, text=f"Number of AI wins: {self.ai_wins}")
        self.ai_wins_label.pack()

    def update_scoreboard(self):
        self.x_wins_label.config(text=f"Number of Player X wins: {self.x_wins}")
        self.ai_wins_label.config(text=f"Number of AI wins: {self.ai_wins}")

    def on_click(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner():
                if self.current_player == "X":
                    self.x_wins += 1
                else:
                    self.ai_wins += 1
                messagebox.showinfo("Tic Tac Toe", f"Player {self.current_player} wins!")
                self.update_scoreboard()
                self.save_scores()
                self.reset_game()
            elif self.check_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw! Nobody wins!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O":
                    self.make_ai_move()

    def make_ai_move(self):
        # AI movement using import random
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = "O"
            self.buttons[row][col].config(text="O")
            if self.check_winner():
                self.ai_wins += 1
                messagebox.showinfo("Tic Tac Toe", "AI wins! Would you like to try again?")
                self.update_scoreboard()
                self.reset_game()
            elif self.check_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw! Nobody wins!")
                self.reset_game()
            else:
                self.current_player = "X"

    def check_winner(self):
        # checks the rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return True
        # checks the columns
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != "":
                return True
        # checks the diagonals
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] != "") or \
           (self.board[0][2] == self.board[1][1] == self.board[2][0] != ""):
            return True
        return False

    def check_draw(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    return False
        return True

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ""
                self.buttons[i][j].config(text="")
        self.current_player = "X"

    def reset_scoreboard(self):
        self.x_wins = 0
        self.ai_wins = 0
        self.update_scoreboard()
        self.save_scores()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
