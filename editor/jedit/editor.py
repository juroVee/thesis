# package-level modules
from .gui import Board
from .gui import Logger
from .util import NotSupportedException, hide_interactive_toolbars, check_parameters
from .config import config

# external modules
from matplotlib import get_backend
from IPython.display import display


class Editor:

    def __init__(self):
        self.board = None
        self.logger = Logger()

    def run(self, **params):
        if not config['editor_settings']['figure_header'] == 'yes':
            hide_interactive_toolbars()
        if 'inline' in get_backend():
            raise NotSupportedException('Clause %matplotlib inline is not supported. Please use %matplotlib notebook.')
        self.board = Board(check_parameters(params, self.logger), self.logger)
        plot = self.board.get_plot_object()
        display(self.board.get_widget())

        with plot.output:
            plot.update()

# run instance after importing editor
editor = Editor()


