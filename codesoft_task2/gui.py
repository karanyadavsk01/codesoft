import tkinter as tk
from tkinter import messagebox

from ai import best_move


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe AI")
        self.root.geometry("420x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#151922")

        self.colors = {
            "bg": "#151922",
            "panel": "#202636",
            "tile": "#2b3346",
            "tile_hover": "#35405a",
            "text": "#f4f7fb",
            "muted": "#aab4c5",
            "player": "#4dd4ac",
            "ai": "#ff7a90",
            "accent": "#6ea8fe",
            "accent_hover": "#8bbaff",
            "danger": "#ff5f6d",
            "danger_hover": "#ff7c88",
        }

        self.board = [""] * 9
        self.buttons = []
        self.cell_size = 96
        self.cell_gap = 8
        self.board_size = (self.cell_size * 3) + (self.cell_gap * 2)
        self.player_score = 0
        self.ai_score = 0
        self.draw_score = 0
        self.rounds = 0

        title = tk.Label(
            root,
            text="Tic Tac Toe AI",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        title.pack(pady=(18, 8))

        self.status = tk.Label(
            root,
            text="Your Turn (X)",
            font=("Segoe UI", 13, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["player"]
        )
        self.status.pack(pady=5)

        scoreboard = tk.Frame(root, bg=self.colors["bg"])
        scoreboard.pack(pady=10)

        self.rounds_label = tk.Label(
            scoreboard,
            text="Round: 0",
            font=("Segoe UI", 11, "bold"),
            width=12,
            bg=self.colors["panel"],
            fg=self.colors["text"],
            padx=6,
            pady=8
        )
        self.rounds_label.grid(row=0, column=0, padx=5, pady=5)

        self.player_score_label = tk.Label(
            scoreboard,
            text="Player: 0",
            font=("Segoe UI", 11, "bold"),
            width=12,
            bg=self.colors["panel"],
            fg=self.colors["player"],
            padx=6,
            pady=8
        )
        self.player_score_label.grid(row=0, column=1, padx=5, pady=5)

        self.ai_score_label = tk.Label(
            scoreboard,
            text="AI: 0",
            font=("Segoe UI", 11, "bold"),
            width=12,
            bg=self.colors["panel"],
            fg=self.colors["ai"],
            padx=6,
            pady=8
        )
        self.ai_score_label.grid(row=1, column=0, padx=5, pady=5)

        self.draw_score_label = tk.Label(
            scoreboard,
            text="Draws: 0",
            font=("Segoe UI", 11, "bold"),
            width=12,
            bg=self.colors["panel"],
            fg=self.colors["accent"],
            padx=6,
            pady=8
        )
        self.draw_score_label.grid(row=1, column=1, padx=5, pady=5)

        frame = tk.Frame(
            root,
            width=self.board_size,
            height=self.board_size,
            bg=self.colors["bg"]
        )
        frame.pack(pady=8)
        frame.pack_propagate(False)

        for i in range(9):
            row = i // 3
            column = i % 3
            x_position = column * (self.cell_size + self.cell_gap)
            y_position = row * (self.cell_size + self.cell_gap)

            btn = tk.Button(
                frame,
                text="",
                font=("Segoe UI", 26, "bold"),
                bg=self.colors["tile"],
                fg=self.colors["text"],
                activebackground=self.colors["tile_hover"],
                activeforeground=self.colors["text"],
                highlightthickness=0,
                bd=0,
                relief="flat",
                cursor="hand2",
                command=lambda i=i: self.player_move(i)
            )
            btn.place(
                x=x_position,
                y=y_position,
                width=self.cell_size,
                height=self.cell_size
            )
            self.buttons.append(btn)

        restart = tk.Button(
            root,
            text="Next Round",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["accent"],
            fg="#101522",
            activebackground=self.colors["accent_hover"],
            activeforeground="#101522",
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=8,
            command=self.restart_game
        )
        restart.pack(pady=(20, 8))
        self.add_hover(restart, self.colors["accent"], self.colors["accent_hover"])

        reset_scores = tk.Button(
            root,
            text="Reset Scores",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["danger"],
            fg="#101522",
            activebackground=self.colors["danger_hover"],
            activeforeground="#101522",
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=8,
            command=self.reset_scores
        )
        reset_scores.pack()
        self.add_hover(reset_scores, self.colors["danger"], self.colors["danger_hover"])

    def player_move(self, index):
        if self.board[index] != "":
            return

        self.board[index] = "X"
        self.buttons[index].config(text="X", fg=self.colors["player"])

        result = self.check_winner()

        if result == "X":
            self.record_result("X")
            messagebox.showinfo("Game Over", "You Win!")
            self.restart_game()
            return

        if result == "Draw":
            self.record_result("Draw")
            messagebox.showinfo("Game Over", "It's a Draw!")
            self.restart_game()
            return

        self.ai_move()

    def restart_game(self):
        self.board = [""] * 9

        for btn in self.buttons:
            btn.config(text="", fg=self.colors["text"], bg=self.colors["tile"])

        self.status.config(text="Your Turn (X)")

    def reset_scores(self):
        self.player_score = 0
        self.ai_score = 0
        self.draw_score = 0
        self.rounds = 0
        self.update_scoreboard()
        self.restart_game()

    def record_result(self, result):
        self.rounds += 1

        if result == "X":
            self.player_score += 1
        elif result == "O":
            self.ai_score += 1
        elif result == "Draw":
            self.draw_score += 1

        self.update_scoreboard()

    def update_scoreboard(self):
        self.rounds_label.config(text=f"Round: {self.rounds}")
        self.player_score_label.config(text=f"Player: {self.player_score}")
        self.ai_score_label.config(text=f"AI: {self.ai_score}")
        self.draw_score_label.config(text=f"Draws: {self.draw_score}")

    def add_hover(self, button, normal_color, hover_color):
        button.bind("<Enter>", lambda event: button.config(bg=hover_color))
        button.bind("<Leave>", lambda event: button.config(bg=normal_color))

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for combo in winning_combinations:
            a, b, c = combo

            if self.board[a] == self.board[b] == self.board[c] != "":
                return self.board[a]

        if "" not in self.board:
            return "Draw"

        return None

    def ai_move(self):
        move = best_move(self.board)

        if move is None:
            return

        self.board[move] = "O"
        self.buttons[move].config(text="O", fg=self.colors["ai"])

        result = self.check_winner()

        if result == "O":
            self.record_result("O")
            messagebox.showinfo("Game Over", "AI Wins!")
            self.restart_game()
        elif result == "Draw":
            self.record_result("Draw")
            messagebox.showinfo("Game Over", "It's a Draw!")
            self.restart_game()
