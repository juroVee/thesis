from .gui import Board
from .misc import PlotNotSetException
from matplotlib.figure import Figure
from matplotlib.axes import Axes

class Editor:

    def __init__(self):
        self.board = None


    def run(self, fig, ax):
        check_fig = isinstance(fig, Figure)
        check_ax = isinstance(ax, Axes)
        if not any([check_fig, check_ax]):
            raise PlotNotSetException('No correct figure or axes provided. Check types of fig and ax.')
        self.board = Board(fig, ax)
        return self.board.get()