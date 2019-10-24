from .gui import Board
from .misc import PlotNotSetException, NotSupportedException
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib import get_backend
from IPython.display import display


class Editor:

    def __init__(self):
        self.user_fig, self.user_ax = None, None
        self.board = None

    def run(self, fig, ax):
        self.user_fig, self.user_ax = fig, ax
        check_fig = isinstance(fig, Figure)
        check_ax = isinstance(ax, Axes)

        if not any([check_fig, check_ax]):
            raise PlotNotSetException('No correct figure or axes provided. Check types of fig and ax.')
        if 'inline' in get_backend():
            raise NotSupportedException('Clause %matplotlib inline is not supported. Please use %matplotlib notebook.')


        self.board = Board(fig, ax)
        plot = self.board.get_plot()
        display(self.board.get_widget())

        with plot.output:
            #clear_output()
            plot.update()
