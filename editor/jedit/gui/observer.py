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
        self.manager.update_plot(main=True, derivatives=True, zero_points=True)
        function = self.manager.get_current()
        message = f'Function changed to {choice}.'
        if function.get_parameter('zero_points_method') != 'none':
            n_zp_values = len(function.get_parameter('zero_points_values'))
            if len(function.get_parameter('user_derivatives')) > 0:
                method = function.get_parameter('zero_points_method')
                message += f'\nPlotting zero points calculated by {method.upper()} method ({n_zp_values}).'
            else:
                message += f'\nNo user derivatives provided.\nPlotting zero points calculated by SECANT method ({n_zp_values}).'
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
        self.logger.write_mini('Recalculating function...')
        self.manager.update_plot(main=True, derivatives=True, zero_points=True)
        message = f'Refinement set to {b["new"]} of it\'s original'
        if function.get_parameter('zero_points_method') != 'none':
            method = function.get_parameter('zero_points_method')
            n_zp_values = len(function.get_parameter('zero_points_values'))
            message += f'\nPlotting zero points calculated by {method.upper()} method ({n_zp_values}).'
        self.logger.write_mini(message)
        self.logger.write(message)
        self._log_zero_points()

    def _changed_zero_points(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('zero_points_method', choice)
        self.configuration.save('zero_points_method', choice)
        self.manager.update_plot(zero_points=True)
        if choice == 'none':
            message = 'Zero points removed from the plot'
            self.logger.write_mini(message)
            self.logger.write(message)
            return
        zero_points = function.get_parameter('zero_points_values')
        if len(function.get_parameter('user_derivatives')) == 0:
            message1 = f'No user derivatives provided.\nPlotting zero points calculated by SECANT method ({len(zero_points)}).'
        else:
            message1 = f'Plotting zero points calculated by {choice.upper()} method ({len(zero_points)}).'
        if len(zero_points) > 0:
            message2 = f'{len(zero_points)} zero point(s) found: \n\t[{", ".join(self._format(zero_points))}]'
        else:
            message2 = f'No zero points found'
        self.logger.write_mini(message1)
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

    def _changed_zero_points_iterations(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('zero_points_iterations', choice)
        self.configuration.save('zero_points_iterations', choice)
        self.manager.update_plot(zero_points=True)
        message = f'Zero points iterations changed to {str(choice)}'
        if function.get_parameter('zero_points_method') != 'none':
            method = function.get_parameter('zero_points_method')
            n_zp_values = len(function.get_parameter('zero_points_values'))
            message += f'\nPlotting zero points calculated by {method.upper()} method ({n_zp_values}).'
        self.logger.write_mini(message)
        self.logger.write(message)
        self._log_zero_points()

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

        gui_elements['text']['zp_iterations'].observe(self._changed_zero_points_iterations, 'value')

        #gui_elements['dropdown']['zp_derivatives_signs'].observe(self._changed_zero_points_derivative_signs, 'value')