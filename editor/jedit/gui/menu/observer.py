import numpy as np

from .util import logger_message, Configuration
from ...config import config


class Observer:
    """
    Class Observer handles user interaction with editor and contains methods 
    which serve as actions after user interaction.
    """

    def __init__(self, board):
        self.function_manager = board.get_object('function_manager')
        self.menu = board.get_object('main_menu')
        self.logger = board.get_object('logger')
        self.logger.write(logger_message('editor spustený'), main=True)
        self.write_warnings()
        self.configuration = Configuration()
        self.rules = {'vypnuté': False, 'zapnuté': True}
        self.svk = {True: 'áno', False: 'nie'}

    def write_warnings(self) -> None:
        """
        Method sends all the warnings generated during computations to logger object which prints them to the log
        """
        warnings = self.function_manager.get_warnings()
        while not warnings.empty():
            warning = warnings.get()
            self.logger.write(logger_message('upozornenie',
                                             správa=str(warning.message),
                                             kategória=str(warning.category),
                                             súbor=str(warning.filename)), warnings=True)

    def _add_zero_points_info(self, function, refinement_support=False) -> None:
        """
        Handles all the information about zero points and sends them to logger object which prints them to the log
        :param function: A function object
        :param refinement_support: Condition to print information about zero points after refinement change
        :return: 
        """
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
        zp_values = np.concatenate(list(dataset.values()))
        message_mini = logger_message('nulové body', viditeľné=self.svk[visible],
                                      derivácia="áno" if method == "Newton" else "nie",
                                      metóda=method,
                                      maxiter=maxiter,
                                      počet=len(zp_values))
        message = logger_message('nulové body', viditeľné=self.svk[visible],
                                 derivácia="áno" if method == "Newton" else "nie",
                                 metóda=method,
                                 maxiter=maxiter,
                                 počet=len(zp_values),
                                 hodnoty=zp_values)
        if not refinement_support:
            self.logger.write(message_mini, mini=True)
        self.logger.write(message, main=True)

    def _add_extremes_info(self, function, refinement_support=False) -> None:
        """
        Handles all the information about extremes and sends them to logger object which prints them to the log
        :param function: A function object
        :param refinement_support: Condition to print information about extremes after refinement change
        :return: 
        """
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

    def _add_inflex_points_info(self, function, refinement_support=False) -> None:
        """
        Handles all the information about inflex points and sends them to logger object which prints them to the log
        :param function: A function object
        :param refinement_support: Condition to print information about inflex points after refinement change
        :return: 
        """
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

    def _add_analysis_info(self, function, op='increasing', refinement_support=False) -> None:
        """
        Handles all the information about monotonic and convex intervals and sends them to logger 
        object which prints them to the log
        :param function: A function object
        :param refinement_support: Condition to print information about monotonic and convex intervals
        after refinement change
        :return: 
        """
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

    def _changed_grid(self, event) -> None:
        """
        Event handler that turns plotting grid on or off
        :param event: A data structure which saves user input information
        :return:
        """
        visible = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('grid', visible)
        self.configuration.save('grid', visible)
        self.function_manager.update_plot()
        message = logger_message('mriežka', viditeľné=self.svk[visible])
        self.logger.write(message, main=True, mini=True)

    def _changed_logger_order(self, event) -> None:
        """
        Event handler that revereses logs print order
        :param event: A data structure which saves user input information
        :return:
        """
        message = logger_message('výpisy', poradie=event['new'])
        self.logger.set_order_oldest(True if event['new'] == 'od najstaršieho' else False)
        self.logger.write(message, main=True, mini=True)

    def _changed_logger_save(self, event) -> None:
        """
        Event handler that saves log to file
        :param event: A data structure which saves user input information
        :return:
        """
        file_name = self.logger.to_file()
        message = logger_message('výpisy', stav='uložené', súbor=file_name)
        self.logger.write(message, mini=True)

    def _changed_derivative1(self, event) -> None:
        """
        Event handler that turns plotting first derivative on or off
        :param event: A data structure which saves user input information
        :return:
        """
        visible = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('active_derivative1', visible)
        self.configuration.save('active_derivative1', visible)
        self.function_manager.update_plot()
        message = logger_message('prvá derivácia', viditeľné=self.svk[visible])
        self.logger.write(message, main=True, mini=True)

    def _changed_derivative2(self, event) -> None:
        """
        Event handler that turns plotting second derivative on or off
        :param event: A data structure which saves user input information
        :return:
        """
        visible = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('active_derivative2', visible)
        self.configuration.save('active_derivative2', visible)
        self.function_manager.update_plot()
        message = logger_message('druhá derivácia', viditeľné=self.svk[visible])
        self.logger.write(message, main=True, mini=True)

    def _changed_derivative3(self, event) -> None:
        """
        Event handler that turns plotting third derivative on or off
        :param event: A data structure which saves user input information
        :return:
        """
        visible = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('active_derivative3', visible)
        self.configuration.save('active_derivative3', visible)
        self.function_manager.update_plot()
        message = logger_message('tretia derivácia', viditeľné=self.svk[visible])
        self.logger.write(message, main=True, mini=True)

    def _changed_color_main_function(self, event) -> None:
        """
        Event handler that changes color of main function
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('main_function_color', choice)
        self.configuration.save('main_function_color', choice)
        self.function_manager.update_plot()
        message = logger_message('hlavná funkcia', farba=choice)
        self.logger.write(message, main=True, mini=True)

    def _changed_color_derivative1(self, event) -> None:
        """
        Event handler that changes color of first derivative
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('derivative_color1', choice)
        self.configuration.save('derivative_color1', choice)
        self.function_manager.update_plot()
        message = logger_message('prvá derivácia', farba=choice)
        self.logger.write(message, main=True, mini=True)

    def _changed_color_derivative2(self, event) -> None:
        """
        Event handler that changes color of second derivative
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('derivative_color2', choice)
        self.configuration.save('derivative_color2', choice)
        self.function_manager.update_plot()
        message = logger_message('druhá derivácia', farba=choice)
        self.logger.write(message, main=True, mini=True)

    def _changed_color_derivative3(self, event) -> None:
        """
        Event handler that changes color of third derivative
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('derivative_color3', choice)
        self.configuration.save('derivative_color3', choice)
        self.function_manager.update_plot()
        self.logger.write(logger_message('tretia derivácia', farba=choice), main=True, mini=True)

    def _changed_refinement_x(self, event) -> None:
        """
        Event handler that changes refinement of x axis
        :param event: A data structure which saves user input information
        :return:
        """
        options = {value + 'x': int(value) for value in config['refinement_x']['values'] if value != 'pôvodné'}
        options['pôvodné'] = 1
        choice = options[event['new']]
        function = self.function_manager.get_current()
        function.set_refinement_x(choice)
        self.configuration.save('refinement_x', choice)
        self.logger.write('Prepočítavanie funkcie...', timer=True)
        self.function_manager.update_plot(main_function=True, derivatives=True, zero_points=True, extremes=True,
                                          inflex_points=True, monotonic=True, convex=True)
        n_x_values = sum(map(len, function.get_parameter("x_values")))
        message = logger_message('zjemnenie x-ovej osi', zjemnenie=event['new'], počet_intervalov=n_x_values - 1,
                                 počet_hodnôt=n_x_values)
        self.logger.write(message, main=True, mini=True)
        self._add_zero_points_info(function, refinement_support=True)
        self._add_extremes_info(function, refinement_support=True)
        self._add_inflex_points_info(function, refinement_support=True)
        self._add_analysis_info(function, refinement_support=True)

    def _changed_refinement_y(self, b) -> None:
        options = {value + 'x': int(value) for value in config['refinement_y']['values'] if value != 'pôvodné'}
        options['pôvodné'] = 1
        choice = options[b['new']]
        function = self.function_manager.get_current()
        function.set_parameter('refinement_y', choice)
        self.logger.write('Prepočítavanie funkcie...', timer=True)
        self.function_manager.update_plot(zero_points=True)
        message = logger_message('zjemnenie y-ovej osi', zjemnenie=b['new'])
        self.logger.write(message, main=True, mini=True)
        self._add_zero_points_info(function, refinement_support=True)

    def _changed_zero_points(self, event) -> None:
        """
        Event handler that turns plotting zero points on or off
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('zero_points_visible', choice)
        if choice:
            function.set_parameter('zero_points_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        self.configuration.save('zero_points_visible', choice)
        self.function_manager.update_plot()
        self._add_zero_points_info(function)

    def _changed_color_zero_points(self, event) -> None:
        """
        Event handler that changes color of zero_points
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('zero_points_color', choice)
        self.configuration.save('zero_points_color', choice)
        self.function_manager.update_plot()
        self.logger.write(logger_message('nulové body', farba=choice), main=True, mini=True)

    def _changed_iterations(self, event) -> None:
        """
        Event handler that changes maximum number of iterations for the Newton Method
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('zero_points_iterations', choice)
        self.configuration.save('zero_points_iterations', choice)
        self.function_manager.update_plot(zero_points=True)
        self._add_zero_points_info(function)

    def _changed_extremes(self, event) -> None:
        """
        Event handler that turns plotting extremes on or off
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        if choice:
            function.set_parameter('extremes_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set_parameter('extremes_visible', choice)
        self.configuration.save('extremes_visible', choice)
        self.function_manager.update_plot()
        self._add_extremes_info(function)

    def _changed_color_extremes(self, event) -> None:
        """
        Event handler that changes color of extremes
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('extremes_color', choice)
        self.configuration.save('extremes_color', choice)
        self.function_manager.update_plot()
        self.logger.write(logger_message('extrémy', farba=choice), main=True, mini=True)

    def _changed_inflex_points(self, event) -> None:
        """
        Event handler that turns plotting inflex points on or off
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        if choice:
            function.set_parameter('inflex_points_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set_parameter('inflex_points_visible', choice)
        self.configuration.save('inflex_points_visible', choice)
        self.function_manager.update_plot()
        self._add_inflex_points_info(function)

    def _changed_color_inflex_points(self, event) -> None:
        """
        Event handler that changes color of inflex points
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('inflex_points_color', choice)
        self.configuration.save('inflex_points_color', choice)
        self.function_manager.update_plot()
        self.logger.write(logger_message('inflexné body', farba=choice), main=True, mini=True)

    def _changed_increasing(self, event) -> None:
        """
        Event handler that turns plotting increasing monotonic interval on or off
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        if choice:
            function.set_parameter('increasing_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set_parameter('increasing_visible', choice)
        self.configuration.save('increasing_visible', choice)
        self.function_manager.update_plot()
        self._add_analysis_info(function, op='increasing')

    def _changed_color_increasing(self, event) -> None:
        """
        Event handler that changes color of increasing monotonic interval
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('increasing_color', choice)
        self.configuration.save('increasing_color', choice)
        self.function_manager.update_plot()
        self.logger.write(logger_message('rastúca', farba=choice), main=True, mini=True)

    def _changed_decreasing(self, event) -> None:
        """
        Event handler that turns plotting decreasing monotonic interval on or off
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        if choice:
            function.set_parameter('decreasing_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set_parameter('decreasing_visible', choice)
        self.configuration.save('decreasing_visible', choice)
        self.function_manager.update_plot()
        self._add_analysis_info(function, op='decreasing')

    def _changed_color_decreasing(self, event) -> None:
        """
        Event handler that changes color of decreasing monotonic interval
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('decreasing_color', choice)
        self.configuration.save('decreasing_color', choice)
        self.function_manager.update_plot()
        self.logger.write(logger_message('klesajúca', farba=choice), main=True, mini=True)

    def _changed_convex(self, event) -> None:
        """
        Event handler that turns plotting convex interval on or off
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        if choice:
            function.set_parameter('convex_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set_parameter('convex_visible', choice)
        self.configuration.save('convex_visible', choice)
        self.function_manager.update_plot()
        self._add_analysis_info(function, op='convex')

    def _changed_color_convex(self, event) -> None:
        """
        Event handler that changes color of convex interval
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('convex_color', choice)
        self.configuration.save('convex_color', choice)
        self.function_manager.update_plot()
        self.logger.write(logger_message('konvexná', farba=choice), main=True, mini=True)

    def _changed_concave(self, event) -> None:
        """
        Event handler that turns plotting concave interval on or off
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        if choice:
            function.set_parameter('concave_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set_parameter('concave_visible', choice)
        self.configuration.save('concave_visible', choice)
        self.function_manager.update_plot()
        self._add_analysis_info(function, op='concave')

    def _changed_color_concave(self, event) -> None:
        """
        Event handler that changes color of concave interval
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_current()
        function.set_parameter('concave_color', choice)
        self.configuration.save('concave_color', choice)
        self.function_manager.update_plot()
        self.logger.write(logger_message('konkávna', farba=choice), main=True, mini=True)

    def start(self) -> None:
        """
        Starts observing for all the menu elements and waits for user action
        :return:
        """
        gui_elements = self.menu.get_elements()

        for element in gui_elements['hbox']:
            dropdown, color_picker = gui_elements['hbox'][element].children
            if hasattr(self, f'_changed_{element}'):
                dropdown.observe(getattr(self, f'_changed_{element}'), 'value')
            if hasattr(self, f'_changed_color_{element}'):
                color_picker.observe(getattr(self, f'_changed_color_{element}'), 'value')

        for element in gui_elements['toggle']:
            button = gui_elements['toggle'][element].children[0]
            if hasattr(self, f'_changed_{element}'):
                button.observe(getattr(self, f'_changed_{element}'), 'value')

        for element in gui_elements['dropdown']:
            _, dropdown = gui_elements['dropdown'][element].children
            if hasattr(self, f'_changed_{element}'):
                dropdown.observe(getattr(self, f'_changed_{element}'), 'value')

        for element in gui_elements['text']:
            _, text = gui_elements['text'][element].children
            if hasattr(self, f'_changed_{element}'):
                text.observe(getattr(self, f'_changed_{element}'), 'value')

        for element in gui_elements['button']:
            button = gui_elements['button'][element].children[0]
            if hasattr(self, f'_changed_{element}'):
                button.on_click(getattr(self, f'_changed_{element}'))
