from .gui import Board
from .util import NotSupportedException
from .config import FIGURE_HEADER
from matplotlib import get_backend
from IPython.display import display, HTML


class Editor:

    def __init__(self):
        self.board = None

    def run(self, fig=None, ax=None):
        if 'inline' in get_backend():
            raise NotSupportedException('Clause %matplotlib inline is not supported. Please use %matplotlib notebook.')
        self.board = Board(fig, ax)
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
