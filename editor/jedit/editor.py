from .gui import Board
from .util import NotSupportedException, hide_interactive_toolbars, get_user_parameters
from .config import FIGURE_HEADER
from matplotlib import get_backend
from IPython.display import display, clear_output


class Editor:

    def __init__(self):
        self.board = None

    def run(self, figure=None, axis=None, function=None, *X_values):
        if not FIGURE_HEADER:
            hide_interactive_toolbars()
        if 'inline' in get_backend():
            raise NotSupportedException('Clause %matplotlib inline is not supported. Please use %matplotlib notebook.')
        self.board = Board(get_user_parameters(figure, axis, function, X_values))
        plot = self.board.get_plot()
        display(self.board.get_widget())

        with plot.output:
            plot.update()

# run instance after importing editor

editor = Editor()

