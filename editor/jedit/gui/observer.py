from ..config import config

def logger_message(theme, **kwargs):
    return theme, kwargs


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
        self.logger.write(logger_message('editor spustený'), main=True)
        self.write_warnings()
        self.configuration = self.Configuration()
        self.rules = {'vypnuté': False, 'zapnuté': True}
        self.svk = {True: 'áno', False: 'nie'}

    def write_warnings(self):
        warnings = self.manager.get_warnings()
        while not warnings.empty():
            warning_type, warning, not_conv, zero_der = warnings.get()
            self.logger.write(logger_message('upozornenie',
                                             správa=str(warning.message),
                                             kategória=str(warning.category),
                                             súbor=str(warning.filename),
                                             nekonvergované=not_conv,
                                             nulová_derivácia=zero_der), warnings=True)

    def _add_zero_points_info(self, function):
        self.write_warnings()
        visible = function.get_parameter('zero_points_visible')
        zp_values = function.get_parameter('zero_points_values')
        method = function.get_parameter('zero_points_method')
        maxiter = function.get_parameter('zero_points_iterations')
        if not visible:
            self.logger.write(logger_message('nulové body', viditeľné=self.svk[visible],
                                      derivácia="áno" if method == "Newton" else "nie",
                                      metóda=method,
                                      maxiter=maxiter), mini=True, main=True)
            return
        message_mini = logger_message('nulové body', viditeľné=self.svk[visible],
                                      derivácia="áno" if method == "Newton" else "nie",
                                      metóda=method,
                                      maxiter=maxiter,
                                      nájdené=len(zp_values))
        message = logger_message('nulové body', viditeľné=self.svk[visible],
                                   derivácia="áno" if method == "Newton" else "nie",
                                   metóda=method,
                                   maxiter=maxiter,
                                   nájdené=zp_values)
        self.logger.write(message_mini, mini=True)
        self.logger.write(message, main=True)

    def _add_extremes_info(self, function):
        visible = function.get_parameter('extremes_visible')
        if not visible:
            self.logger.write(logger_message('extrémy', viditeľné=self.svk[visible]), mini=True, main=True)
            return
        minX = function.get_parameter('local_minima_xvals')
        maxX = function.get_parameter('local_maxima_xvals')
        minY = function.get_parameter('local_minima_yvals')
        maxY = function.get_parameter('local_maxima_yvals')
        coords_min = list(zip(minX, minY))
        coords_max = list(zip(maxX, maxY))
        message_mini = logger_message('extrémy', viditeľné=self.svk[visible],
                                       extrémy=len(coords_min) + len(coords_max),
                                       lokálne_minimá=len(coords_min),
                                       lokálne_maximá=len(coords_max))
        message = logger_message('extrémy', viditeľné=self.svk[visible],
                                 lokálne_minimá=coords_min,
                                 lokálne_maximá=coords_max)
        self.logger.write(message_mini, mini=True)
        self.logger.write(message, main=True)

    def _add_inflex_points_info(self, function):
        visible = function.get_parameter('inflex_points_visible')
        if not visible:
            self.logger.write(logger_message('inflexné body', viditeľné=self.svk[visible]), mini=True, main=True)
            return
        foundX = function.get_parameter('inflex_points_xvals')
        foundY = function.get_parameter('inflex_points_yvals')
        coords = list(zip(foundX, foundY))
        message_mini = logger_message('inflexné body', viditeľné=self.svk[visible], nájdené=len(coords))
        message = logger_message('inflexné body', viditeľné=self.svk[visible], nájdené=coords)
        self.logger.write(message_mini, mini=True)
        self.logger.write(message, main=True)

    def _changed_function(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        if choice == 'užívateľ':
            choice = 'user function'
        self.manager.set_current(choice)
        self.manager.apply_configuration(self.configuration.get())
        self.manager.update_plot(main=True, derivatives=True, zero_points=True, extremes=True, inflex_points=True)
        self.write_warnings()
        message = logger_message('hlavná funkcia', voľba=b['new'])
        self.logger.write(message, main=True, mini=True)

    def _changed_grid(self, b) -> None:
        self.manager.set_plot_updated(True)
        visible = self.rules[b['new']]
        function = self.manager.get_current()
        function.set_parameter('grid', visible)
        self.configuration.save('grid', visible)
        self.manager.update_plot()
        message = logger_message('mriežka', viditeľné=self.svk[visible])
        self.logger.write(message, main=True, mini=True)

    def _changed_derivative1(self, b) -> None:
        self.manager.set_plot_updated(True)
        visible = self.rules[b['new']]
        function = self.manager.get_current()
        function.set_parameter('active_derivative1', visible)
        self.configuration.save('active_derivative1', visible)
        self.manager.update_plot()
        message = logger_message('prvá derivácia', viditeľné=self.svk[visible])
        self.logger.write(message, main=True, mini=True)

    def _changed_derivative2(self, b) -> None:
        self.manager.set_plot_updated(True)
        visible = self.rules[b['new']]
        function = self.manager.get_current()
        function.set_parameter('active_derivative2', visible)
        self.configuration.save('active_derivative2', visible)
        self.manager.update_plot()
        message = logger_message('druhá derivácia', viditeľné=self.svk[visible])
        self.logger.write(message, main=True, mini=True)

    def _changed_derivative3(self, b) -> None:
        self.manager.set_plot_updated(True)
        visible = self.rules[b['new']]
        function = self.manager.get_current()
        function.set_parameter('active_derivative3', visible)
        self.configuration.save('active_derivative3', visible)
        self.manager.update_plot()
        message = logger_message('tretia derivácia', viditeľné=self.svk[visible])
        self.logger.write(message, main=True, mini=True)

    def _changed_color_main(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('main_function_color', choice)
        self.configuration.save('main_function_color', choice)
        self.manager.update_plot()
        message = logger_message('hlavná funkcia', farba=choice)
        self.logger.write(message, main=True, mini=True)

    def _changed_color_derivative1(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('derivative_color1', choice)
        self.configuration.save('derivative_color1', choice)
        self.manager.update_plot()
        message = logger_message('prvá derivácia', farba=choice)
        self.logger.write(message, main=True, mini=True)

    def _changed_color_derivative2(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('derivative_color2', choice)
        self.configuration.save('derivative_color2', choice)
        self.manager.update_plot()
        message = logger_message('druhá derivácia', farba=choice)
        self.logger.write(message, main=True, mini=True)

    def _changed_color_derivative3(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('derivative_color3', choice)
        self.configuration.save('derivative_color3', choice)
        self.manager.update_plot()
        self.logger.write(logger_message('tretia derivácia', farba=choice), main=True, mini=True)

    def _changed_refinement(self, b) -> None:
        self.manager.set_plot_updated(True)
        options = {**{'pôvodné' : 1}, **{str(value) + 'x': value for value in config['refinement']['values']}}
        choice = options[b['new']]
        function = self.manager.get_current()
        function.set_refinement(choice)
        self.configuration.save('refinement', choice)
        self.logger.write(logger_message('Prepočítavanie funkcie...'), mini=True)
        self.manager.update_plot(main=True, derivatives=True, zero_points=True, extremes=True, inflex_points=True)
        n_x_values = sum(map(len, function.get_parameter("x_values")))
        message = logger_message('zjemnenie x-ovej osi', zjemnenie=b['new'], počet_intervalov=n_x_values-1, počet_hodnôt=n_x_values)
        self.logger.write(message, main=True, mini=True)

    def _changed_zero_points(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = self.rules[b['new']]
        function = self.manager.get_current()
        function.set_parameter('zero_points_visible', choice)
        self.configuration.save('zero_points_visible', choice)
        self.manager.update_plot()
        self._add_zero_points_info(function)

    def _changed_zero_points_color(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('zero_points_color', choice)
        self.configuration.save('zero_points_color', choice)
        self.manager.update_plot()
        self.logger.write(logger_message('nulové body', mini=True, farba=choice), main=True, mini=True)

    def _changed_zero_points_iterations(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('zero_points_iterations', choice)
        self.configuration.save('zero_points_iterations', choice)
        self.manager.update_plot(zero_points=True)
        self._add_zero_points_info(function)

    def _changed_extremes_points(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = self.rules[b['new']]
        function = self.manager.get_current()
        function.set_parameter('extremes_visible', choice)
        self.configuration.save('extremes_visible', choice)
        self.manager.update_plot()
        self._add_extremes_info(function)

    def _changed_extremes_color(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('extremes_color', choice)
        self.configuration.save('extremes_color', choice)
        self.manager.update_plot()
        self.logger.write(logger_message('extrémy', mini=True, farba=choice), main=True, mini=True)

    def _changed_inflex_points(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = self.rules[b['new']]
        function = self.manager.get_current()
        function.set_parameter('inflex_points_visible', choice)
        self.configuration.save('inflex_points_visible', choice)
        self.manager.update_plot()
        self._add_inflex_points_info(function)

    def _changed_inflex_points_color(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('inflex_points_color', choice)
        self.configuration.save('inflex_points_color', choice)
        self.manager.update_plot()
        self.logger.write(logger_message('inflexné body', mini=True, farba=choice), main=True, mini=True)

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