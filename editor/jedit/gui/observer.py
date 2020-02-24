from ..config import config

def logger_message(theme: str, **kwargs):
    return f'\n{theme}: {kwargs}'

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
        self.logger.write(message='Session started', main=True)
        self.write_warnings()
        self.configuration = self.Configuration()

    def _add_zero_points_info(self, function, message, message_mini):
        self.write_warnings()
        visible = function.get_parameter('zero_points_visible')
        if not visible:
            self.logger.write(message, main=True, mini=True)
            return
        zp_values = function.get_parameter('zero_points_values')
        method = function.get_parameter('zero_points_method')
        maxiter = function.get_parameter('zero_points_iterations')
        message_mini += logger_message('Zero points', visible=visible, found=len(zp_values), user_fprime="Yes" if method == "Newton" else "No", method=method, maxiter=maxiter)
        message = logger_message('Zero points', values=zp_values)
        self.logger.write(message_mini, main=True, mini=True)
        self.logger.write(message, main=True)

    def _add_extremes_info(self, function, message, message_mini):
        visible = function.get_parameter('extremes_visible')
        if not visible:
            self.logger.write(message, main=True, mini=True)
            return
        local_minima = function.get_parameter('local_minima')
        local_maxima = function.get_parameter('local_maxima')
        global_minima = function.get_parameter('global_minima')[1] if function.get_parameter('global_minima') != [] else []
        global_maxima = function.get_parameter('global_maxima')[1] if function.get_parameter('global_maxima') != [] else []
        message_mini += logger_message('Extremes', visible=visible,
                                       extremes=len(local_minima) + len(local_maxima),
                                       minima=len(local_minima),
                                       maxima=len(local_maxima))
        message = logger_message('Extremes', visible=visible,
                                 local_minima=[y for x, y in local_minima],
                                 local_maxima=[y for x, y in local_maxima],
                                 global_minima=global_minima,
                                 global_maxima=global_maxima)
        self.logger.write(message_mini, main=True, mini=True)
        self.logger.write(message, main=True)

    def _add_inflex_points_info(self, function, message, message_mini):
        visible = function.get_parameter('inflex_points_visible')
        if not visible:
            self.logger.write(message, main=True, mini=True)
            return
        found = function.get_parameter('inflex_points_values')
        message_mini += logger_message('Inflex points', visible=visible, found=len(found))
        message = logger_message('Inflex points', visible=visible, found=found)
        self.logger.write(message_mini, main=True, mini=True)
        self.logger.write(message, main=True)

    def write_warnings(self):
        warnings = self.manager.get_warnings()
        while not warnings.empty():
            warning_type, warning, not_conv, zero_der = warnings.get()
            message = str(warning.message)
            if message == 'some derivatives were zero':
                message = f'{warning_type}:\n\tDerivatives at point(s) {zero_der} were zero.'
            elif message.startswith('some failed to converge after'):
                message = f'{warning_type}:\n\tMethod {message[5:]} at point(s) {not_conv}.'
            else:
                message = f'{warning_type}: {warning.message}'
            self.logger.write(message, warnings=True)

    def _changed_function(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        self.manager.set_current(choice)
        self.manager.apply_configuration(self.configuration.get())
        self.manager.update_plot(main=True, derivatives=True, zero_points=True)
        self.write_warnings()
        function = self.manager.get_current()
        message = logger_message('Main function', set=choice)
        self._add_zero_points_info(function, message, message)

    def _changed_grid(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = True if b['new'] == 'true' else False
        function = self.manager.get_current()
        function.set_parameter('grid', choice)
        self.configuration.save('grid', choice)
        self.manager.update_plot()
        message = logger_message('Grid', visible=choice)
        self.logger.write(message, main=True, mini=True)

    def _changed_derivative1(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = True if b['new'] == 'true' else False
        function = self.manager.get_current()
        function.set_parameter('active_derivative1', choice)
        self.configuration.save('active_derivative1', choice)
        self.manager.update_plot()
        message = logger_message('1st derivative', visible=choice)
        self.logger.write(message, main=True, mini=True)

    def _changed_derivative2(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = True if b['new'] == 'true' else False
        function = self.manager.get_current()
        function.set_parameter('active_derivative2', choice)
        self.configuration.save('active_derivative2', choice)
        self.manager.update_plot()
        message = logger_message('2nd derivative', visible=choice)
        self.logger.write(message, main=True, mini=True)

    def _changed_derivative3(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = True if b['new'] == 'true' else False
        function = self.manager.get_current()
        function.set_parameter('active_derivative3', choice)
        self.configuration.save('active_derivative3', choice)
        self.manager.update_plot()
        message = logger_message('3rd derivative', visible=choice)
        self.logger.write(message, main=True, mini=True)

    def _changed_color_main(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('main_function_color', choice)
        self.configuration.save('main_function_color', choice)
        self.manager.update_plot()
        message = logger_message('Main function', color=choice)
        self.logger.write(message, main=True, mini=True)

    def _changed_color_derivative1(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('derivative_color1', choice)
        self.configuration.save('derivative_color1', choice)
        self.manager.update_plot()
        message = logger_message('1st derivative', color=choice)
        self.logger.write(message, main=True, mini=True)

    def _changed_color_derivative2(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('derivative_color2', choice)
        self.configuration.save('derivative_color2', choice)
        self.manager.update_plot()
        message = logger_message('2nd derivative', color=choice)
        self.logger.write(message, main=True, mini=True)

    def _changed_color_derivative3(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('derivative_color3', choice)
        self.configuration.save('derivative_color3', choice)
        self.manager.update_plot()
        message = logger_message('3rd derivative', color=choice)
        self.logger.write(message, main=True, mini=True)

    def _changed_refinement(self, b) -> None:
        self.manager.set_plot_updated(True)
        options = {**{'original' : 1}, **{str(value) + 'x': value for value in config['refinement']['values']}}
        choice = options[b['new']]
        function = self.manager.get_current()
        function.set_refinement(choice)
        self.configuration.save('refinement', choice)
        self.logger.write('Recalculating function...', mini=True)
        self.manager.update_plot(main=True, derivatives=True, zero_points=True, extremes=True, inflex_points=True)
        n_x_values = sum(map(len, function.get_parameter("x_values")))
        message = logger_message('Refinement', refinement=b['new'], intervals=n_x_values-1, values=n_x_values)
        self._add_zero_points_info(function, message, message)
        self._add_extremes_info(function, message, message)
        self._add_inflex_points_info(function, message, message)

    def _changed_zero_points(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('zero_points_visible', choice)
        self.configuration.save('zero_points_visible', choice)
        self.manager.update_plot()
        self._add_zero_points_info(function, '', '')

    def _changed_zero_points_color(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('zero_points_color', choice)
        self.configuration.save('zero_points_color', choice)
        self.manager.update_plot()
        self.logger.write(logger_message('Zero points', color=choice), main=True, mini=True)

    def _changed_zero_points_iterations(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('zero_points_iterations', choice)
        self.configuration.save('zero_points_iterations', choice)
        self.manager.update_plot(zero_points=True)
        self._add_zero_points_info(function, '', '')

    def _changed_extremes_points(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('extremes_visible', choice)
        self.configuration.save('extremes_visible', choice)
        self.manager.update_plot()
        self._add_extremes_info(function, '', '')

    def _changed_extremes_color(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('extremes_color', choice)
        self.configuration.save('extremes_color', choice)
        self.manager.update_plot()
        self.logger.write(logger_message('Extremes', color=choice), main=True, mini=True)

    def _changed_inflex_points(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('inflex_points_visible', choice)
        self.configuration.save('inflex_points_visible', choice)
        self.manager.update_plot()
        self._add_inflex_points_info(function, '', '')

    def _changed_inflex_points_color(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('inflex_points_color', choice)
        self.configuration.save('inflex_points_color', choice)
        self.manager.update_plot()
        self.logger.write(logger_message('Inflex points', color=choice), main=True, mini=True)

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

        dropdown, color_picker = gui_elements['hbox']['extremes'].children
        dropdown.observe(self._changed_extremes_points, 'value')
        color_picker.observe(self._changed_extremes_color, 'value')

        dropdown, color_picker = gui_elements['hbox']['inflex_points'].children
        dropdown.observe(self._changed_inflex_points, 'value')
        color_picker.observe(self._changed_inflex_points_color, 'value')

        gui_elements['text']['zp_iterations'].observe(self._changed_zero_points_iterations, 'value')