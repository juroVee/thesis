from IPython.display import clear_output
from .sidebar_elements import (color_picker,
                               dropdown_grid,
                               dropdown_functions,
                               dropdown_functions_not_defined,
                               dropdown_derivative)

class Observer:

    def __init__(self, board):
        self.plot = board.get_plot()
        self.carousel = self.plot.carousel

    def _changed_function(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        self.carousel.set_current(self.carousel[choice])
        with self.plot.output:
            clear_output()
            self.plot.update()

    def _changed_grid(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        for function in self.carousel.get_all():
            function.set_grid(choice)
        with self.plot.output:
            clear_output()
            self.plot.update()

    def _changed_derivative(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        for function in self.carousel.get_all():
            function.set_derivative_plot(choice)
        with self.plot.output:
            clear_output()
            self.plot.update()


    def _changed_color(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        for function in self.carousel.get_all():
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
        dropdown_derivative.observe(self._changed_derivative, 'value')
        color_picker.observe(self._changed_color, 'value')