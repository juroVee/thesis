from IPython.display import clear_output
from .sidebar_elements import (color_picker,
                               dropdown_grid,
                               dropdown_functions,
                               dropdown_functions_not_defined,
                               dropdown_aspect)

class Observer:

    def __init__(self, board):
        self.board = board
        self.plot = self.board.plot

    def _changed_function(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        self.plot.current_function = self.plot.functions[choice]
        with self.plot.output:
            clear_output()
            self.plot.update()

    def _changed_grid(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        functions =  self.plot.functions.values()
        for function in functions:
            function.set_grid(choice)
        with self.plot.output:
            clear_output()
            self.plot.update()

    def _changed_aspect(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        functions =  self.plot.functions.values()
        for function in functions:
            function.set_aspect(choice)
        with self.plot.output:
            clear_output()
            self.plot.update()

    def _changed_color(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        functions = self.plot.functions.values()
        for function in functions:
            function.set_color(choice)
        with self.plot.output:
            clear_output()
            self.plot.update()


    def start(self) -> None:
        if self.plot.is_user_defined():
            dropdown_functions.observe(self._changed_function, 'value')
        else:
            dropdown_functions_not_defined.observe(self._changed_function, 'value')
        dropdown_grid.observe(self._changed_grid, 'value')
        dropdown_aspect.observe(self._changed_aspect, 'value')
        color_picker.observe(self._changed_color, 'value')