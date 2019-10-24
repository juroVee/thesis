from IPython.display import clear_output
from .sidebar_elements import color_picker, dropdown_grid, dropdown_functions, dropdown_functions_not_defined
from ..config import DEFAULT_FUNCTIONS

class Observer:

    def __init__(self, board):
        self.board = board
        self.plot = self.board.plot

    def _changed_function(self, b) -> None:
        choice = b['new']
        if choice == 'user defined':
            self.plot.user_defined = True
        else:
            self.plot.user_defined = False
            function = DEFAULT_FUNCTIONS[choice]['function']
            linspace = DEFAULT_FUNCTIONS[choice]['linspace']
            latex = DEFAULT_FUNCTIONS[choice]['latex']
            self.plot.defined_function = function, latex, linspace
        self.plot.updated = True
        with self.plot.output:
            clear_output()
            self.plot.update()

    def _changed_grid(self, b) -> None:
        self.plot.grid = True if b['new'] == 'True' else False
        self.plot.updated = True
        with self.plot.output:
            clear_output()
            self.plot.update()

    def _changed_color(self, b) -> None:
        self.plot.color = b['new']
        self.plot.updated = True
        with self.plot.output:
            clear_output()
            self.plot.update()

    def start(self) -> None:
        if self.plot.user_defined:
            dropdown_functions.observe(self._changed_function, 'value')
        else:
            dropdown_functions_not_defined.observe(self._changed_function, 'value')
        dropdown_grid.observe(self._changed_grid, 'value')
        color_picker.observe(self._changed_color, 'value')

