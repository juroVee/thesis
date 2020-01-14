import numpy as np
import pprint

from ..config import config


class Observer:

    class Configuration:

        def __init__(self):
            self.configuration = {}

        def get(self):
            return self.configuration

        def save(self, parameter, value):
            self.configuration[parameter] = value

    def __init__(self, board):
        self.plot = board.get_plot_object()
        self.logger = board.get_logger_object()
        self.gui_manager = board.get_gui_manager_object()
        self.logger.write('Session started')
        self.function_manager = self.plot.function_manager
        self.configuration = self.Configuration()

    def _format(self, data):
        output = []
        for i, val in enumerate(data):
            if (i + 1) % 7 == 0:
                output.append(f'\n{str(val)}')
            else:
                output.append(str(val))
        return output

    def _changed_function(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        self.function_manager.set_current(self.function_manager[choice])
        self.function_manager.apply_configuration(self.configuration.get())
        self.plot.update()
        message = f'Function changed to {choice}'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_grid(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        function = self.function_manager.get_current()
        function.set_parameter('grid', choice)
        self.configuration.save('grid', choice)
        self.plot.update()
        self.logger.write('Grid visible' if choice else 'Grid hidden')

    def _changed_derivative1(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        function = self.function_manager.get_current()
        function.set_parameter('active_derivative1', choice)
        self.configuration.save('active_derivative1', choice)
        self.plot.update()
        message = 'Plotting 1. derivative' if choice else '1. derivative plot removed'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_derivative2(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        function = self.function_manager.get_current()
        function.set_parameter('active_derivative2', choice)
        self.configuration.save('active_derivative2', choice)
        self.plot.update()
        message = 'Plotting 2. derivative' if choice else '2. derivative plot removed'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_derivative3(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        function = self.function_manager.get_current()
        function.set_parameter('active_derivative3', choice)
        self.configuration.save('active_derivative3', choice)
        self.plot.update()
        message = 'Plotting 3. derivative' if choice else '3. derivative plot removed'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_color_main(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        function = self.function_manager.get_current()
        function.set_parameter('main_function_color', choice)
        self.configuration.save('main_function_color', choice)
        self.plot.update()
        message = f'Color of main function changed to {choice}'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_color_derivative1(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        function = self.function_manager.get_current()
        function.set_parameter('derivative_color1', choice)
        self.configuration.save('derivative_color1', choice)
        self.plot.update()
        message = f'Color of 1. derivative changed to {choice}'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_color_derivative2(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        function = self.function_manager.get_current()
        function.set_parameter('derivative_color2', choice)
        self.configuration.save('derivative_color2', choice)
        self.plot.update()
        message = f'Color of 2. derivative changed to {choice}'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_color_derivative3(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        function = self.function_manager.get_current()
        function.set_parameter('derivative_color3', choice)
        self.configuration.save('derivative_color3', choice)
        self.plot.update()
        message = f'Color of 3. derivative changed to {choice}'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_refinement(self, b) -> None:
        self.plot.updated = True
        options = {**{'original' : 1}, **{str(value) + 'x': value for value in config['refinement']['values']}}
        choice = options[b['new']]
        function = self.function_manager.get_current()
        function.set_refinement(choice)
        function.recalculate_main_function()
        function.recalculate_derivatives()
        self.configuration.save('refinement', choice)
        self.plot.update()
        message = f'Refinement set to {b["new"]} of it\'s original'
        self.logger.write_mini(message)
        self.logger.write(message)
        if function.get_parameter('zero_points_method') != 'none':
            zp_sorted = np.sort(list(function.get_parameter('zero_points_values')), axis=None)
            if len(zp_sorted) > 0:
                message2 = f'Zero points found: \n\t[{", ".join(self._format(zp_sorted))}]'
                self.logger.write(message2)

    def _changed_zero_points(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        function = self.function_manager.get_current()
        function.set_parameter('zero_points_method', choice)
        self.configuration.save('zero_points_method', choice)
        self.plot.update()
        if choice == 'none':
            message = 'Zero points removed from the plot'
            self.logger.write_mini(message)
            self.logger.write(message)
            return
        zp_sorted = np.sort(list(function.get_parameter('zero_points_values')), axis=None)
        message1 = f'Plotting zero points using {choice.upper()} method ({len(zp_sorted)})'
        if len(zp_sorted) > 0:
            message2 = f'Zero points found: \n\t[{", ".join(self._format(zp_sorted))}]'
        else:
            message2 = f'No zero points found'
        self.logger.write_mini(message1)
        self.logger.write(message1)
        self.logger.write(message2)

    def _changed_zero_points_color(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        function = self.function_manager.get_current()
        function.set_parameter('zero_points_color', choice)
        self.configuration.save('zero_points_color', choice)
        self.plot.update()
        message = f'Color of zero points changed to {choice}'
        self.logger.write_mini(message)
        self.logger.write(message)

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