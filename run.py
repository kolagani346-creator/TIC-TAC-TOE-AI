import kivy
kivy.require("2.1.0")

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.clock import Clock
import math


LabelBase.register(
    name="Emoji",
    fn_regular="C:/Windows/Fonts/seguiemj.ttf"
)


def check_winner(board, player):

    wins = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for row in wins:

        if all(board[i] == player for i in row):
            return True

    return False


def is_full(board):
    return " " not in board


def minimax(board, depth, maximize):

    if check_winner(board, "O"):
        return 10 - depth

    if check_winner(board, "X"):
        return depth - 10

    if is_full(board):
        return 0

    if maximize:

        best = -math.inf

        for i in range(9):

            if board[i] == " ":

                board[i] = "O"

                score = minimax(
                    board,
                    depth + 1,
                    False
                )

                board[i] = " "

                best = max(
                    best,
                    score
                )

        return best

    else:

        best = math.inf

        for i in range(9):

            if board[i] == " ":

                board[i] = "X"

                score = minimax(
                    board,
                    depth + 1,
                    True
                )

                board[i] = " "

                best = min(
                    best,
                    score
                )

        return best


def best_move(board):

    best = -math.inf

    move = -1

    for i in range(9):

        if board[i] == " ":

            board[i] = "O"

            score = minimax(
                board,
                0,
                False
            )

            board[i] = " "

            if score > best:

                best = score
                move = i

    return move


class TicTacToe(App):

    def build(self):

        Window.size = (430, 650)

        self.board = [" "] * 9

        self.game_over = False

        root = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        self.title_label = Label(
            text="🎮 TIC TAC TOE 🎮",
            font_name="Emoji",
            font_size=32,
            size_hint=(1, .18)
        )

        self.grid = GridLayout(
            cols=3,
            size_hint=(None, None),
            size=(390, 390),
            spacing=8,
            padding=10
        )

        self.buttons = []

        for i in range(9):

            btn = Button(
                text="",
                font_size=60,
                bold=True,
                size_hint=(None, None),
                size=(120, 120)
            )

            btn.bind(
                on_press=lambda x, i=i:
                self.make_move(i)
            )

            self.grid.add_widget(btn)

            self.buttons.append(btn)

        root.add_widget(
            self.title_label
        )

        root.add_widget(
            self.grid
        )

        return root

    def make_move(self, pos):

        if self.game_over:
            return

        if self.board[pos] != " ":
            return

        self.board[pos] = "X"

        self.buttons[pos].text = "X"

        if self.finish():
            return

        self.ai_move()

    def ai_move(self):

        move = best_move(
            self.board
        )

        if move != -1:

            self.board[move] = "O"

            self.buttons[move].text = "O"

        self.finish()

    def finish(self):

        if check_winner(
            self.board,
            "X"
        ):

            self.game_over = True

            self.popup(
                "🏆 YOU WIN 🏆"
            )

            return True

        if check_winner(
            self.board,
            "O"
        ):

            self.game_over = True

            self.popup(
                "🤖 AI WINS 🤖"
            )

            return True

        if is_full(
            self.board
        ):

            self.game_over = True

            self.popup(
                "🤝 DRAW 🤝"
            )

            return True

        return False

    def popup(self, text):

        popup = Popup(
            title="🎮 TIC TAC TOE",
            content=Label(
                text=text,
                font_name="Emoji",
                font_size=30
            ),
            size_hint=(None, None),
            size=(350, 250)
        )

        popup.open()

        Clock.schedule_once(
            lambda dt:
            (
                popup.dismiss(),
                self.reset_game()
            ),
            2
        )

    def reset_game(self):

        self.board = [" "] * 9

        self.game_over = False

        for btn in self.buttons:

            btn.text = ""

        self.title_label.text = "🎮 TIC TAC TOE 🎮"


if __name__ == "__main__":

    TicTacToe().run()
