from .gui import Board
from .util import NotSupportedException, check_params
from .config import FIGURE_HEADER
from matplotlib import get_backend
from IPython.display import display, HTML


class Editor:

    def __init__(self):
        self.board = None

    def run(self, figure=None, axis=None, function=None, *X_values):
        if 'inline' in get_backend():
            raise NotSupportedException('Clause %matplotlib inline is not supported. Please use %matplotlib notebook.')

        check_params(figure, axis, function, X_values)
        self.board = Board(user_data=(figure, axis, function, X_values))
        plot = self.board.get_plot()
        display(self.board.get_widget())

        with plot.output:
            plot.update()

# run instance after importing editor

editor = Editor()

if not FIGURE_HEADER:
    html = '''
        <style>
        .cell .output_wrapper .ui-dialog-titlebar {
          display: none;
        }    
        </style>
        '''
    display(HTML(html))
