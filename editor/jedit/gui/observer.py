from IPython.display import clear_output
from .sidebar_elements import color_picker, dropdown_grid

class Observer:

    def __init__(self, board):
        self.board = board
        self.plot = self.board.plot

    def _changed_grid(self, b) -> None:
        self.plot.grid = True if b['new'] == 'True' else False
        self.plot.updated = True
        with self.plot.output:
            clear_output()
            self.plot.plot_function()

    def _changed_color(self, b) -> None:
        self.plot.color = b['new']
        self.plot.updated = True
        with self.plot.output:
            clear_output()
            self.plot.plot_function()

    def start(self) -> None:
        dropdown_grid.observe(self._changed_grid, 'value')
        color_picker.observe(self._changed_color, 'value')

