from ..config import config

def logger_message(theme: str, newline, **kwargs):
    if newline:
        return f'\n{theme}: {kwargs}'
    return f'{theme}: {kwargs}'

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

    def _changed_function(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        self.manager.set_current(choice)
        self.manager.apply_configuration(self.configuration.get())
        self.manager.update_plot(main=True, derivatives=True, zero_points=True)
        self.manager.get_warnings(self.logger)
        function = self.manager.get_current()
        message_mini = logger_message('Main function', False, set=choice)
        message = logger_message('Main function', False, set=choice)
        visible = function.get_parameter('zero_points_visible')
        if not visible:
            self.logger.write_mini(message)
            self.logger.write(message)
            return
        zp_values = function.get_parameter('zero_points_values')
        n_zp_values = len(zp_values)
        method = function.get_parameter('zero_points_method')
        maxiter = function.get_parameter('zero_points_iterations')
        message_mini += logger_message('Roots', True, visible=visible, found=n_zp_values, fprime="Yes" if method == "Newton" else "No", method=method, maxiter=maxiter)
        message += logger_message('Roots', True, visible=visible, found=n_zp_values, fprime="Yes" if method == "Newton" else "No", method=method, maxiter=maxiter, values=zp_values)
        self.logger.write_mini(message_mini)
        self.logger.write(message)

    def _changed_grid(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = True if b['new'] == 'true' else False
        function = self.manager.get_current()
        function.set_parameter('grid', choice)
        self.configuration.save('grid', choice)
        self.manager.update_plot()
        message = logger_message('Grid', False, visible=choice)
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_derivative1(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = True if b['new'] == 'true' else False
        function = self.manager.get_current()
        function.set_parameter('active_derivative1', choice)
        self.configuration.save('active_derivative1', choice)
        self.manager.update_plot()
        message = logger_message('1st derivative', False, visible=choice)
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_derivative2(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = True if b['new'] == 'true' else False
        function = self.manager.get_current()
        function.set_parameter('active_derivative2', choice)
        self.configuration.save('active_derivative2', choice)
        self.manager.update_plot()
        message = logger_message('2nd derivative', False, visible=choice)
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_derivative3(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = True if b['new'] == 'true' else False
        function = self.manager.get_current()
        function.set_parameter('active_derivative3', choice)
        self.configuration.save('active_derivative3', choice)
        self.manager.update_plot()
        message = logger_message('3rd derivative', False, visible=choice)
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_color_main(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('main_function_color', choice)
        self.configuration.save('main_function_color', choice)
        self.manager.update_plot()
        message = logger_message('Main function', False, color=choice)
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_color_derivative1(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('derivative_color1', choice)
        self.configuration.save('derivative_color1', choice)
        self.manager.update_plot()
        message = logger_message('1st derivative', False, color=choice)
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_color_derivative2(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('derivative_color2', choice)
        self.configuration.save('derivative_color2', choice)
        self.manager.update_plot()
        message = logger_message('2nd derivative', False, color=choice)
        self.logger.write_mini(message)
        self.logger.write(message)

    def _changed_color_derivative3(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('derivative_color3', choice)
        self.configuration.save('derivative_color3', choice)
        self.manager.update_plot()
        message = logger_message('3rd derivative', False, color=choice)
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
        visible = function.get_parameter('zero_points_visible')
        n_x_values = sum(map(len, function.get_parameter("x_values")))
        message_mini = logger_message('Refinement', False, refinement=b['new'], intervals=n_x_values-1, values=n_x_values)
        message = logger_message('Refinement', False, refinement=b['new'], intervals=n_x_values-1, values=n_x_values)
        if not visible:
            self.logger.write_mini(message)
            self.logger.write(message)
            return
        zp_values = function.get_parameter('zero_points_values')
        n_zp_values = len(zp_values)
        method = function.get_parameter('zero_points_method')
        maxiter = function.get_parameter('zero_points_iterations')
        message_mini += logger_message('Roots', True, visible=visible, found=n_zp_values, fprime="Yes" if method == "Newton" else "No", method=method, maxiter=maxiter)
        message += logger_message('Roots', True, visible=visible, found=n_zp_values, fprime="Yes" if method == "Newton" else "No", method=method, maxiter=maxiter, values=zp_values)
        self.logger.write_mini(message_mini)
        self.logger.write(message)

    def _changed_zero_points(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('zero_points_visible', choice)
        self.configuration.save('zero_points_visible', choice)
        self.manager.update_plot(zero_points=True)
        if not choice:
            self.logger.write_mini(logger_message('Roots', False, visible=choice))
            self.logger.write(logger_message('Roots', False, visible=choice))
            return
        zp_values = function.get_parameter('zero_points_values')
        n_zp_values = len(zp_values)
        method = function.get_parameter('zero_points_method')
        maxiter = function.get_parameter('zero_points_iterations')
        message_mini = logger_message('Roots', False, visible=True, found=n_zp_values, fprime="Yes" if method == "Newton" else "No", method=method, maxiter=maxiter)
        message = logger_message('Roots', False, visible=True, found=n_zp_values, fprime="Yes" if method == "Newton" else "No", method=method, maxiter=maxiter, values=zp_values)
        self.logger.write_mini(message_mini)
        self.logger.write(message)

    def _changed_zero_points_color(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('zero_points_color', choice)
        self.configuration.save('zero_points_color', choice)
        self.manager.update_plot()
        self.logger.write_mini(logger_message('Roots', False, color=choice))
        self.logger.write(logger_message('Roots', False, color=choice))

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
        visible = function.get_parameter('zero_points_visible')
        if not visible:
            self.logger.write_mini(logger_message('Roots', False, maxiter=choice))
            self.logger.write(logger_message('Roots', False, maxiter=choice))
            return
        zp_values = function.get_parameter('zero_points_values')
        n_zp_values = len(zp_values)
        method = function.get_parameter('zero_points_method')
        maxiter = function.get_parameter('zero_points_iterations')
        message_mini = logger_message('Roots', False, visible=True, found=n_zp_values, fprime="Yes" if method == "Newton" else "No", method=method, maxiter=maxiter)
        message = logger_message('Roots', False, visible=True, found=n_zp_values, fprime="Yes" if method == "Newton" else "No", method=method, maxiter=maxiter, values=zp_values)
        self.logger.write_mini(message_mini)
        self.logger.write(message)

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