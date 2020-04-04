import numpy as np

from ..config import config
from ..util import flatten

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
            warning = warnings.get()
            self.logger.write(logger_message('upozornenie',
                                             správa=str(warning.message),
                                             kategória=str(warning.category),
                                             súbor=str(warning.filename)), warnings=True)

    def _add_zero_points_info(self, function, refinement_support=False):
        self.write_warnings()
        visible = function.get_parameter('zero_points_visible')
        dataset = function.get_parameter('zero_points_dataset')
        method = function.get_parameter('zero_points_method')
        maxiter = function.get_parameter('zero_points_iterations')
        if not visible:
            if not refinement_support:
                self.logger.write(logger_message('nulové body', viditeľné=self.svk[visible],
                                          derivácia="áno" if method == "Newton" else "nie",
                                          metóda=method,
                                          maxiter=maxiter), mini=True, main=True)
            return
        zp_values = flatten(dataset)
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
        if not refinement_support:
            self.logger.write(message_mini, mini=True)
        self.logger.write(message, main=True)

    def _add_extremes_info(self, function, refinement_support=False):
        visible = function.get_parameter('extremes_visible')
        if not visible:
            if not refinement_support:
                self.logger.write(logger_message('extrémy', viditeľné=self.svk[visible]), mini=True, main=True)
            return
        dataset = function.get_parameter('extremes_dataset')
        minX = np.asarray(np.concatenate([extremes['minima'] for extremes in dataset.values()])).flatten()
        maxX = np.asarray(np.concatenate([extremes['maxima'] for extremes in dataset.values()])).flatten()
        full = np.sort(np.concatenate([minX, maxX]))
        message_mini = logger_message('extrémy', viditeľné=self.svk[visible],
                                       ostré_lokálne_extrémy=len(full))
        message = logger_message('extrémy', viditeľné=self.svk[visible],
                                 ostré_lokálne_extrémy_v_bodoch=full,
                                 ostré_lokálne_minimá_v_bodoch=minX,
                                 ostré_lokálne_maximá_v_bodoch=maxX)
        if not refinement_support:
            self.logger.write(message_mini, mini=True)
        self.logger.write(message, main=True)

    def _add_inflex_points_info(self, function, refinement_support=False):
        visible = function.get_parameter('inflex_points_visible')
        if not visible:
            if not refinement_support:
                self.logger.write(logger_message('inflexné body', viditeľné=self.svk[visible]), mini=True, main=True)
            return
        dataset = function.get_parameter('inflex_points_dataset')
        full = np.sort(np.asarray(np.concatenate(list(dataset.values()))).flatten())
        message_mini = logger_message('inflexné body', viditeľné=self.svk[visible], nájdené=len(full))
        message = logger_message('inflexné body', viditeľné=self.svk[visible], v_bodoch=full)
        if not refinement_support:
            self.logger.write(message_mini, mini=True)
        self.logger.write(message, main=True)

    def _add_analysis_info(self, function, op='increasing', refinement_support=False):
        visible = function.get_parameter(f'{op}_visible')
        desc = {'increasing': 'rastúca',
                'decreasing': 'klesajúca',
                'convex': 'konvexná',
                'concave': 'konkávna'}
        if not visible:
            if not refinement_support:
                self.logger.write(logger_message(desc[op], viditeľné=self.svk[visible]), mini=True, main=True)
            return
        dataset = function.get_parameter(f'{op}_dataset')
        pairs = []
        for dct in dataset.values():
            for pair in dct['intervals']:
                pairs.append(pair)
        message_mini = logger_message(desc[op], viditeľné=self.svk[visible], nájdené_intervaly_x=len(pairs))
        message = logger_message(desc[op], viditeľné=self.svk[visible], intervaly_x=pairs)
        if not refinement_support:
            self.logger.write(message_mini, mini=True)
        self.logger.write(message, main=True)

    def _changed_grid(self, b) -> None:
        self.manager.set_plot_updated(True)
        visible = b['new']
        function = self.manager.get_current()
        function.set_parameter('grid', visible)
        self.configuration.save('grid', visible)
        self.manager.update_plot()
        message = logger_message('mriežka', viditeľné=self.svk[visible])
        self.logger.write(message, main=True, mini=True)

    def _changed_derivative1(self, b) -> None:
        self.manager.set_plot_updated(True)
        visible = b['new']
        function = self.manager.get_current()
        function.set_parameter('active_derivative1', visible)
        self.configuration.save('active_derivative1', visible)
        self.manager.update_plot()
        message = logger_message('prvá derivácia', viditeľné=self.svk[visible])
        self.logger.write(message, main=True, mini=True)

    def _changed_derivative2(self, b) -> None:
        self.manager.set_plot_updated(True)
        visible = b['new']
        function = self.manager.get_current()
        function.set_parameter('active_derivative2', visible)
        self.configuration.save('active_derivative2', visible)
        self.manager.update_plot()
        message = logger_message('druhá derivácia', viditeľné=self.svk[visible])
        self.logger.write(message, main=True, mini=True)

    def _changed_derivative3(self, b) -> None:
        self.manager.set_plot_updated(True)
        visible = b['new']
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
        self.logger.write('Prepočítavanie funkcie...', timer=True)
        self.manager.update_plot(main_function=True, derivatives=True, zero_points=True, extremes=True, inflex_points=True, monotonic=True, convex=True)
        n_x_values = sum(map(len, function.get_parameter("x_values")))
        message = logger_message('zjemnenie x-ovej osi', zjemnenie=b['new'], počet_intervalov=n_x_values-1, počet_hodnôt=n_x_values)
        self.logger.write(message, main=True, mini=True)
        self._add_zero_points_info(function, refinement_support=True)
        self._add_extremes_info(function, refinement_support=True)
        self._add_inflex_points_info(function, refinement_support=True)
        self._add_analysis_info(function, refinement_support=True)

    def _changed_zero_points(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('zero_points_visible', choice)
        if choice:
            function.set_parameter('zero_points_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
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
        self.logger.write(logger_message('nulové body', farba=choice), main=True, mini=True)

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
        choice = b['new']
        function = self.manager.get_current()
        if choice:
            function.set_parameter('extremes_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
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
        self.logger.write(logger_message('extrémy', farba=choice), main=True, mini=True)

    def _changed_inflex_points(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        if choice:
            function.set_parameter('inflex_points_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
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
        self.logger.write(logger_message('inflexné body', farba=choice), main=True, mini=True)

    def _changed_increasing(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        if choice:
            function.set_parameter('increasing_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set_parameter('increasing_visible', choice)
        self.configuration.save('increasing_visible', choice)
        self.manager.update_plot()
        self._add_analysis_info(function, op='increasing')

    def _changed_increasing_color(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('increasing_color', choice)
        self.configuration.save('increasing_color', choice)
        self.manager.update_plot()
        self.logger.write(logger_message('rastúca', farba=choice), main=True, mini=True)

    def _changed_decreasing(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        if choice:
            function.set_parameter('decreasing_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set_parameter('decreasing_visible', choice)
        self.configuration.save('decreasing_visible', choice)
        self.manager.update_plot()
        self._add_analysis_info(function, op='decreasing')

    def _changed_decreasing_color(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('decreasing_color', choice)
        self.configuration.save('decreasing_color', choice)
        self.manager.update_plot()
        self.logger.write(logger_message('klesajúca', farba=choice), main=True, mini=True)

    def _changed_convex(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        if choice:
            function.set_parameter('convex_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set_parameter('convex_visible', choice)
        self.configuration.save('convex_visible', choice)
        self.manager.update_plot()
        self._add_analysis_info(function, op='convex')

    def _changed_convex_color(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('convex_color', choice)
        self.configuration.save('convex_color', choice)
        self.manager.update_plot()
        self.logger.write(logger_message('konvexná', farba=choice), main=True, mini=True)

    def _changed_concave(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        if choice:
            function.set_parameter('concave_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set_parameter('concave_visible', choice)
        self.configuration.save('concave_visible', choice)
        self.manager.update_plot()
        self._add_analysis_info(function, op='concave')

    def _changed_concave_color(self, b) -> None:
        self.manager.set_plot_updated(True)
        choice = b['new']
        function = self.manager.get_current()
        function.set_parameter('concave_color', choice)
        self.configuration.save('concave_color', choice)
        self.manager.update_plot()
        self.logger.write(logger_message('konkávna', farba=choice), main=True, mini=True)

    def start(self) -> None:
        gui_elements = self.gui_manager.get_elements()

        _, color_picker = gui_elements['function']['main_function'].children
        color_picker.observe(self._changed_color_main, 'value')

        button = gui_elements['function']['grid'].children[0]
        button.observe(self._changed_grid, 'value')

        dropdown, color_picker = gui_elements['function']['derivative1'].children
        dropdown.observe(self._changed_derivative1, 'value')
        color_picker.observe(self._changed_color_derivative1, 'value')

        dropdown, color_picker = gui_elements['function']['derivative2'].children
        dropdown.observe(self._changed_derivative2, 'value')
        color_picker.observe(self._changed_color_derivative2, 'value')

        dropdown, color_picker = gui_elements['function']['derivative3'].children
        dropdown.observe(self._changed_derivative3, 'value')
        color_picker.observe(self._changed_color_derivative3, 'value')

        _, dropdown = gui_elements['analysis']['refinement'].children
        dropdown.observe(self._changed_refinement, 'value')

        dropdown, color_picker = gui_elements['analysis']['zero_points'].children
        dropdown.observe(self._changed_zero_points, 'value')
        color_picker.observe(self._changed_zero_points_color, 'value')

        dropdown, color_picker = gui_elements['analysis']['extremes'].children
        dropdown.observe(self._changed_extremes_points, 'value')
        color_picker.observe(self._changed_extremes_color, 'value')

        dropdown, color_picker = gui_elements['analysis']['inflex_points'].children
        dropdown.observe(self._changed_inflex_points, 'value')
        color_picker.observe(self._changed_inflex_points_color, 'value')

        dropdown, color_picker = gui_elements['analysis']['increasing'].children
        dropdown.observe(self._changed_increasing, 'value')
        color_picker.observe(self._changed_increasing_color, 'value')

        dropdown, color_picker = gui_elements['analysis']['decreasing'].children
        dropdown.observe(self._changed_decreasing, 'value')
        color_picker.observe(self._changed_decreasing_color, 'value')

        dropdown, color_picker = gui_elements['analysis']['convex'].children
        dropdown.observe(self._changed_convex, 'value')
        color_picker.observe(self._changed_convex_color, 'value')

        dropdown, color_picker = gui_elements['analysis']['concave'].children
        dropdown.observe(self._changed_concave, 'value')
        color_picker.observe(self._changed_concave_color, 'value')

        _, dropdown = gui_elements['analysis']['iterations'].children
        dropdown.observe(self._changed_zero_points_iterations, 'value')