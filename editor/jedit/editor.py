from .gui import Board
from .plot import Plot
from .misc import PlotNotSetException


class Editor:

    def __init__(self):
        self._init_GUI()
        self.is_set = False

    def _init_GUI(self):
        self.board = Board()

    def _init_plot(self, fig, ax):
        self.plot = Plot(fig, ax)

    def run(self, fig, ax):
        self._init_plot(fig, ax)
        self.is_set = True
        return self.board.data()