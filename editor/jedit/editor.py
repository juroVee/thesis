from .gui import Board
from .misc import PlotNotSetException
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from IPython.display import display
import ipywidgets as w

html = w.HTML(value='''%%html
<style>
.output_wrapper .ui-dialog-titlebar {
  display: none;
}
</style>''')

class Editor:

    def __init__(self):
        self.board, self.user_fig, self.user_ax = None, None, None
        display(html)


    def run(self, fig, ax):
        self.user_fig, self.user_ax = fig, ax
        check_fig = isinstance(fig, Figure)
        check_ax = isinstance(ax, Axes)
        if not any([check_fig, check_ax]):
            raise PlotNotSetException('No correct figure or axes provided. Check types of fig and ax.')
        self.board = Board(fig, ax)
        return self.board.get_widget()
