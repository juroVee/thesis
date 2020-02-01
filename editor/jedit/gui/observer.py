from ..config import config


class Observer:

    class Configuration:

        def __init__(self):
            self.configuration = {}

        def get(self):
            return self.configuration

        def __getitem__(self, item):
            return self.configuration[item]

        def save(self, parameter, value):
            self.configuration[parameter] = value

    def __init__(self, board):
        self.manager = board.get_manager_object()
        self.logger = board.get_logger_object()
        self.gui_manager = board.get_gui_manager_object()
        self.logger.write('Session started')
        self.manager.get_warnings(self.logger)
        self.configuration = self.Configuration()

    def _format(self, data):
        output = []
        for i, val in enumerate(data):
            if (i + 1) % 7 == 0:
                output.append(f'\n{str(val)}')
            else:
                output.append(str(val))
        return output

    def _log_zero_points(self):
        if 'zero_points_method' in self.configuration.get():
            if self.configuration['zero_points_method'] != 'none':
                zp_sorted = self.manager.get_current().get_parameter('zero_points_values')
                if len(zp_sorted) > 0:
                    message = f'{len(zp_sorted)} zero point(s) found: \n\t[{", ".join(self._format(zp_sorted))}]'
                else:
                    message = f'No zero points found'
                self.logger.write(message)

    def _changed_function(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        self.manager.set_current(choice)
        self.manager.apply_configuration(self.configuration.get())
        self.manager.update_plot(full=True)
        message = f'Function changed to {choice}'
        self.logger.write_mini(message)
        self.logger.write(message)
        self.manager.get_warnings(self.logger)
        self._log_zero_points()

    def _changed_grid(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = True if b['new'] == 'true' else False
        function = self.manager.get_current()
        function.set_parameter('grid', choice)
        self.configuration.save('grid', choice)
        self.manager.update_plot()
        self.logger.write('Grid visible' if choice else 'Grid hidden')

    def _changed_derivative1(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = True if b['new'] == 'true' else False
        function = self.manager.get_current()
        function.set_parameter('active_derivative1', choice)
        self.configuration.save('active_derivative1', choice)
        self.manager.update_plot()
        message = 'Plotting 1. derivative' if choice else '1. derivative plot removed'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_derivative2(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = True if b['new'] == 'true' else False
        function = self.manager.get_current()
        function.set_parameter('active_derivative2', choice)
        self.configuration.save('active_derivative2', choice)
        self.manager.update_plot()
        message = 'Plotting 2. derivative' if choice else '2. derivative plot removed'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_derivative3(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = True if b['new'] == 'true' else False
        function = self.manager.get_current()
        function.set_parameter('active_derivative3', choice)
        self.configuration.save('active_derivative3', choice)
        self.manager.update_plot()
        message = 'Plotting 3. derivative' if choice else '3. derivative plot removed'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_color_main(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('main_function_color', choice)
        self.configuration.save('main_function_color', choice)
        self.manager.update_plot()
        message = f'Color of main function changed to {choice}'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_color_derivative1(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('derivative_color1', choice)
        self.configuration.save('derivative_color1', choice)
        self.manager.update_plot()
        message = f'Color of 1. derivative changed to {choice}'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_color_derivative2(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('derivative_color2', choice)
        self.configuration.save('derivative_color2', choice)
        self.manager.update_plot()
        message = f'Color of 2. derivative changed to {choice}'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_color_derivative3(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('derivative_color3', choice)
        self.configuration.save('derivative_color3', choice)
        self.manager.update_plot()
        message = f'Color of 3. derivative changed to {choice}'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_refinement(self, b) -> None:
        self.manager.set_plot_updated(True)
        options = {**{'original' : 1}, **{str(value) + 'x': value for value in config['refinement']['values']}}
        choice = options[b['new']]
        function = self.manager.get_current()
        function.set_refinement(choice)
        self.configuration.save('refinement', choice)
        self.manager.update_plot(full=True)
        message = f'Refinement set to {b["new"]} of it\'s original'
        self.logger.write_mini(message)
        self.logger.write(message)
        self._log_zero_points()

    def _changed_zero_points(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('zero_points_method', choice)
        self.configuration.save('zero_points_method', choice)
        self.manager.update_plot()
        if choice == 'none':
            message = 'Zero points removed from the plot'
            self.logger.write_mini(message)
            self.logger.write(message)
            return
        # zp_sorted = np.sort(list(function.get_parameter('zero_points_values')), axis=None)
        zp_sorted = function.get_parameter('zero_points_values')
        message1 = f'Plotting zero points using {choice.upper()} method'
        if len(zp_sorted) > 0:
            message2 = f'{len(zp_sorted)} zero point(s) found: \n\t[{", ".join(self._format(zp_sorted))}]'
        else:
            message2 = f'No zero points found'
        self.logger.write_mini(message1 + f' ({len(zp_sorted)})')
        self.logger.write(message1)
        self.logger.write(message2)

    def _changed_zero_points_color(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('zero_points_color', choice)
        self.configuration.save('zero_points_color', choice)
        self.manager.update_plot()
        message = f'Color of zero points changed to {choice}'
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_zero_points_derivative_signs(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = True if b['new'] == 'true' else False
        function = self.manager.get_current()
        function.recalculate_zero_points_derivative_signs()
        self.manager.update_plot()
        if choice:
            if function.get_parameter('zero_points_derivatives_signs') is not None:
                d_signs = function.get_parameter('zero_points_derivatives_signs')
                sorted_keys = sorted(d_signs.keys())
                out = '\n\t'.join([f'{zp}: {d_signs[zp]}' for zp in sorted_keys])
                self.logger.write(f'Printing derivative signs for zero points: \n\t{out}')
            else:
                self.logger.write(f'Printing derivative signs for zero points')
                self.logger.write(f'Zero points need to be calculated first')

    def start(self) -> None:
        gui_elements = self.gui_manager.get_elements()

        dropdown, color_picker = gui_elements['hbox']['function'].children
        dropdown.observe(self._changed_function, 'value')
        color_picker.observe(self._changed_color_main, 'value')

        gui_elements['dropdown']['grid'].observe(self._changed_grid, 'value')

        dropdown, color_picker = gui_elements['hbox']['derivative1'].children
        dropdown.observe(self._changed_derivative1, 'value')
        color_picker.observe(self._changed_color_derivative1, 'value')

        dropdown, color_picker = gui_elements['hbox']['derivative2'].children
        dropdown.observe(self._changed_derivative2, 'value')
        color_picker.observe(self._changed_color_derivative2, 'value')

        dropdown, color_picker = gui_elements['hbox']['derivative3'].children
        dropdown.observe(self._changed_derivative3, 'value')
        color_picker.observe(self._changed_color_derivative3, 'value')

        gui_elements['dropdown']['refinement'].observe(self._changed_refinement, 'value')

        dropdown, color_picker = gui_elements['hbox']['zero_points'].children
        dropdown.observe(self._changed_zero_points, 'value')
        color_picker.observe(self._changed_zero_points_color, 'value')

        #gui_elements['dropdown']['zp_derivatives_signs'].observe(self._changed_zero_points_derivative_signs, 'value')