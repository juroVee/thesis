import numpy as np


class Observer:

    def __init__(self, board):
        self.plot = board.get_plot_object()
        self.logger = board.get_logger_object()
        self.gui_manager = board.get_gui_manager_object()
        self.logger.write('Session started')
        self.function_manager = self.plot.function_manager

    def _changed_function(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        self.function_manager.set_current(self.function_manager[choice])
        self.plot.update()
        self.logger.write(f'Function changed to {choice}')

    def _changed_grid(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        for function in self.function_manager.get_all():
            function.set_parameter('grid', choice)
        self.plot.update()
        self.logger.write('Grid visible' if choice else 'Grid hidden')

    def _changed_derivative1(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        for function in self.function_manager.get_all():
            function.show_derivative(1, choice)
        self.plot.update()
        self.logger.write('Plotting 1. derivative' if choice else '1. derivative plot removed')

    def _changed_derivative2(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        for function in self.function_manager.get_all():
            function.show_derivative(2, choice)
        self.plot.update()
        self.logger.write('Plotting 2. derivative' if choice else '2. derivative plot removed')

    def _changed_derivative3(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        for function in self.function_manager.get_all():
            function.show_derivative(3, choice)
        self.plot.update()
        self.logger.write('Plotting 3. derivative' if choice else '3. derivative plot removed')

    def _changed_color_main(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        for function in self.function_manager.get_all():
            function.set_parameter('main_function_color', choice)
        self.plot.update()
        self.logger.write(f'Color of main function changed to {choice}')

    def _changed_color_derivative1(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        for function in self.function_manager.get_all():
            function.set_parameter('derivative_colors', choice, sub=1)
        self.plot.update()
        self.logger.write(f'Color of 1. derivative changed to {choice}')

    def _changed_color_derivative2(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        for function in self.function_manager.get_all():
            function.set_parameter('derivative_colors', choice, sub=2)
        self.plot.update()
        self.logger.write(f'Color of 2. derivative changed to {choice}')

    def _changed_color_derivative3(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        for function in self.function_manager.get_all():
            function.set_parameter('derivative_colors', choice, sub=3)
        self.plot.update()
        self.logger.write(f'Color of 3. derivative changed to {choice}')

    def _changed_refinement(self, b) -> None:
        self.plot.updated = True
        options = {'original':0, '10x':1, '100x':2, '1000x':3, '10000x':4}
        choice = options[b['new']]
        for function in self.function_manager.get_all():
            function.set_refinement(choice)
            function.recalculate_derivatives()
        self.plot.update()
        self.logger.write(f'Refinement set to {b["new"]} of it\'s original')

    def _changed_zero_points(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        for function in self.function_manager.get_all():
            function.set_parameter('zero_points_method', choice)
        self.plot.update()
        current = self.function_manager.get_current()
        current_zero_points = np.around(sorted(current.get_parameter('zero_points_values')), decimals=4)
        if choice != 'none':
            self.logger.write(f'Plotting zero points using {choice.upper()} method\n{current_zero_points}')

    def _changed_zero_points_color(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        for function in self.function_manager.get_all():
            function.set_parameter('zero_points_color', choice)
        self.plot.update()
        self.logger.write(f'Color of zero points changed to {choice}')

    def start(self) -> None:
        gui_elements = self.gui_manager.get_elements()

        dropdown, color_picker = gui_elements[f'hbox_function'].children
        dropdown.observe(self._changed_function, 'value')
        color_picker.observe(self._changed_color_main, 'value')

        gui_elements['dropdown_grid'].observe(self._changed_grid, 'value')

        dropdown, color_picker = gui_elements[f'hbox_derivative1'].children
        dropdown.observe(self._changed_derivative1, 'value')
        color_picker.observe(self._changed_color_derivative1, 'value')

        dropdown, color_picker = gui_elements[f'hbox_derivative2'].children
        dropdown.observe(self._changed_derivative2, 'value')
        color_picker.observe(self._changed_color_derivative2, 'value')

        dropdown, color_picker = gui_elements[f'hbox_derivative3'].children
        dropdown.observe(self._changed_derivative3, 'value')
        color_picker.observe(self._changed_color_derivative3, 'value')

        gui_elements['dropdown_refinement'].observe(self._changed_refinement, 'value')

        dropdown, color_picker = gui_elements['hbox_zero_points'].children
        dropdown.observe(self._changed_zero_points, 'value')
        color_picker.observe(self._changed_zero_points_color, 'value')