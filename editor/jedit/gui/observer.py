from IPython.display import clear_output
from .sidebar_elements import (color_picker,
                               dropdown_grid,
                               dropdown_functions,
                               dropdown_functions_not_defined,
                               dropdown_derivative1, dropdown_derivative2, dropdown_derivative3,
                               dropdown_refinement)

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

    def _changed_derivative1(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        for function in self.carousel.get_all():
            if choice:
                function.add_derivative(1)
            else:
                function.remove_derivative(1)
        with self.plot.output:
            clear_output()
            self.plot.update()

    def _changed_derivative2(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        for function in self.carousel.get_all():
            if choice:
                function.add_derivative(2)
            else:
                function.remove_derivative(2)
        with self.plot.output:
            clear_output()
            self.plot.update()

    def _changed_derivative3(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        for function in self.carousel.get_all():
            if choice:
                function.add_derivative(3)
            else:
                function.remove_derivative(3)
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

    def _changed_refinement(self, b) -> None:
        self.plot.updated = True
        options = {'original':0, '10x':1, '100x':2, '1000x':3, '10000x':4}
        choice = options[b['new']]
        for function in self.carousel.get_all():
            function.set_refinement(choice)
        with self.plot.output:
            clear_output()
            self.plot.update()


    def start(self) -> None:
        if self.plot.is_user_defined():
            dropdown_functions.observe(self._changed_function, 'value')
        else:
            dropdown_functions_not_defined.observe(self._changed_function, 'value')
        dropdown_grid.observe(self._changed_grid, 'value')
        dropdown_derivative1.observe(self._changed_derivative1, 'value')
        dropdown_derivative2.observe(self._changed_derivative2, 'value')
        dropdown_derivative3.observe(self._changed_derivative3, 'value')
        color_picker.observe(self._changed_color, 'value')
        dropdown_refinement.observe(self._changed_refinement, 'value')