from .gui import Board
from .plots import Plot


class Editor:

    def __init__(self):
        self.board = None

    def run(self, fig, ax):
        self.board = Board(fig, ax)
        return self.board.get()