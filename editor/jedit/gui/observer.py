from ..settings import settings

class Observer:
    """
    Class Observer handles user interaction with editor and contains methods 
    which serve as actions after user interaction.
    """

    def __init__(self, board):
        self.function_manager = board.get_object('function_manager')
        self.menu = board.get_object('main_menu')
        self.logger = board.get_object('logger')
        self.logger.write(self.logger.new_message('editor spustený'), main=True)
        self.rules = {'vypnuté': False, 'zapnuté': True}
        self.svk = {True: 'áno', False: 'nie'}

    def _add_zero_points_info(self, function, refinement_support=False) -> None:
        """
        Handles all the information about zero points and sends them to logger object which prints them to the log
        :param function: A function object
        :param refinement_support: Condition to print information about zero points after refinement change
        :return: 
        """
        visible = function.get('zero_points_visible')
        zero_points = function.get('zero_points')
        method = function.get('zero_points_method')
        maxiter = function.get('zero_points_iterations')
        derivatives_provided = len(function.get('user_derivatives'))
        if not visible:
            if not refinement_support:
                self.logger.write(self.logger.new_message('nulové body',
                                                 derivácie=derivatives_provided,
                                                 metóda=method,
                                                 maxiter=maxiter), mini=True, main=True)
            return
        if not refinement_support:
            self.logger.write(self.logger.new_message('nulové body',
                                      derivácie=derivatives_provided,
                                      metóda=method,
                                      maxiter=maxiter,
                                      počet=len(zero_points)), mini=True)
        self.logger.write(self.logger.new_message('nulové body',
                                 derivácie=derivatives_provided,
                                 metóda=method,
                                 maxiter=maxiter,
                                 počet=len(zero_points),
                                 v_bodoch=zero_points), main=True)

    def _add_extremes_info(self, function, refinement_support=False) -> None:
        """
        Handles all the information about extremes and sends them to logger object which prints them to the log
        :param function: A function object
        :param refinement_support: Condition to print information about extremes after refinement change
        :return: 
        """
        visible = function.get('extremes_visible')
        if not visible:
            if not refinement_support:
                self.logger.write(self.logger.new_message('extrémy', viditeľné=self.svk[visible]), mini=True, main=True)
            return
        minX = function.get('local_minima')
        maxX = function.get('local_maxima')
        full = function.get('local_extrema')
        if not refinement_support:
            self.logger.write(self.logger.new_message('extrémy', viditeľné=self.svk[visible],
                                      ostré_lokálne_extrémy=len(full)), mini=True)
        self.logger.write(self.logger.new_message('extrémy', viditeľné=self.svk[visible],
                                 ostré_lokálne_extrémy_v_bodoch=full,
                                 ostré_lokálne_minimá_v_bodoch=minX,
                                 ostré_lokálne_maximá_v_bodoch=maxX), main=True)

    def _add_inflex_points_info(self, function, refinement_support=False) -> None:
        """
        Handles all the information about inflex points and sends them to logger object which prints them to the log
        :param function: A function object
        :param refinement_support: Condition to print information about inflex points after refinement change
        :return: 
        """
        visible = function.get('inflex_points_visible')
        if not visible:
            if not refinement_support:
                self.logger.write(self.logger.new_message('inflexné body', viditeľné=self.svk[visible]), mini=True, main=True)
            return
        inflex_points = function.get('inflex_points')
        if not refinement_support:
            self.logger.write(self.logger.new_message('inflexné body', viditeľné=self.svk[visible], nájdené=len(inflex_points)), mini=True)
        self.logger.write(self.logger.new_message('inflexné body', viditeľné=self.svk[visible], v_bodoch=inflex_points), main=True)

    def _add_analysis_info(self, function, op='increasing', refinement_support=False) -> None:
        """
        Handles all the information about monotonic and concave intervals and sends them to logger
        object which prints them to the log
        :param function: A function object
        :param refinement_support: Condition to print information about monotonic and concave intervals
        after refinement change
        :return: 
        """
        visible = function.get(f'{op}_visible')
        desc = {'increasing': 'rastúca',
                'decreasing': 'klesajúca',
                'concave_up': 'konvexná',
                'concave_down': 'konkávna'}
        if not visible:
            if not refinement_support:
                self.logger.write(self.logger.new_message(desc[op], viditeľné=self.svk[visible]), mini=True, main=True)
            return

        intervals = function.get(f'{op}_intervals')
        if not refinement_support:
            self.logger.write(self.logger.new_message(desc[op], viditeľné=self.svk[visible], nájdené_intervaly_x=len(intervals)), mini=True)
        self.logger.write(self.logger.new_message(desc[op], viditeľné=self.svk[visible], intervaly_x=intervals), main=True)

    def _changed_grid(self, event) -> None:
        """
        Event handler that turns plotting grid on or off
        :param event: A data structure which saves user input information
        :return:
        """
        visible = event['new']
        function = self.function_manager.get_function()
        function.set('grid', visible)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('mriežka', viditeľné=self.svk[visible]), main=True, mini=True)

    def _changed_logger_order(self, event) -> None:
        """
        Event handler that revereses logs print order
        :param event: A data structure which saves user input information
        :return:
        """
        self.logger.set_order_oldest(True if event['new'] == 'najstaršie' else False)
        self.logger.write(self.logger.new_message('výstupy', poradie=event['new']), main=True, mini=True)

    def _changed_logger_save(self, event) -> None:
        """
        Event handler that saves log to file
        :param event: A data structure which saves user input information
        :return:
        """
        self.logger.write(self.logger.new_message('výstupy', stav='uložené', súbor=self.logger.to_file()), mini=True)

    def _changed_derivative1(self, event) -> None:
        """
        Event handler that turns plotting first derivative on or off
        :param event: A data structure which saves user input information
        :return:
        """
        visible = event['new']
        function = self.function_manager.get_function()
        function.set('active_derivative1', visible)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('prvá derivácia', viditeľné=self.svk[visible]), main=True, mini=True)

    def _changed_derivative2(self, event) -> None:
        """
        Event handler that turns plotting second derivative on or off
        :param event: A data structure which saves user input information
        :return:
        """
        visible = event['new']
        function = self.function_manager.get_function()
        function.set('active_derivative2', visible)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('druhá derivácia', viditeľné=self.svk[visible]), main=True, mini=True)

    def _changed_derivative3(self, event) -> None:
        """
        Event handler that turns plotting third derivative on or off
        :param event: A data structure which saves user input information
        :return:
        """
        visible = event['new']
        function = self.function_manager.get_function()
        function.set('active_derivative3', visible)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('tretia derivácia', viditeľné=self.svk[visible]), main=True, mini=True)

    def _changed_color_main_function(self, event) -> None:
        """
        Event handler that changes color of main function
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('main_function_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('hlavná funkcia', farba=choice), main=True, mini=True)

    def _changed_color_derivative1(self, event) -> None:
        """
        Event handler that changes color of first derivative
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('derivative_color1', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('prvá derivácia', farba=choice), main=True, mini=True)

    def _changed_color_derivative2(self, event) -> None:
        """
        Event handler that changes color of second derivative
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('derivative_color2', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('druhá derivácia', farba=choice), main=True, mini=True)

    def _changed_color_derivative3(self, event) -> None:
        """
        Event handler that changes color of third derivative
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('derivative_color3', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('tretia derivácia', farba=choice), main=True, mini=True)

    def _changed_refinement_x(self, event) -> None:
        """
        Event handler that changes refinement of x axis
        :param event: A data structure which saves user input information
        :return:
        """
        options = {value + 'x': int(value) for value in settings['refinement_x']['values'] if value != 'pôvodné'}
        options['pôvodné'] = 1
        choice = options[event['new']]
        function = self.function_manager.get_function()
        function.set('refinement', choice)
        self.logger.write(self.logger.new_message('Prebieha prepočítavanie funkcie...'), timer=True)
        self.function_manager.update_plot(main_function=True, derivatives=True, zero_points=True, extremes=True,
                                          inflex_points=True, monotonic=True, concave=True)
        n_x_values = sum(map(len, function.get("x_values")))
        self.logger.write(self.logger.new_message('zjemnenie x-ovej osi', zjemnenie=event['new'], počet_intervalov=n_x_values - 1,
                                 počet_hodnôt=n_x_values), main=True, mini=True)
        self._add_zero_points_info(function, refinement_support=True)
        self._add_extremes_info(function, refinement_support=True)
        self._add_inflex_points_info(function, refinement_support=True)
        self._add_analysis_info(function, refinement_support=True)

    def _changed_zero_points(self, event) -> None:
        """
        Event handler that turns plotting zero points on or off
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('zero_points_visible', choice)
        if choice:
            function.set('zero_points_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        self.function_manager.update_plot()
        self._add_zero_points_info(function)

    def _changed_color_zero_points(self, event) -> None:
        """
        Event handler that changes color of zero_points
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('zero_points_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('nulové body', farba=choice), main=True, mini=True)

    def _changed_iterations(self, event) -> None:
        """
        Event handler that changes maximum number of iterations for the Newton Method
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('zero_points_iterations', choice)
        self.function_manager.update_plot(zero_points=True)
        self._add_zero_points_info(function)

    def _changed_rounding(self, event) -> None:
        function = self.function_manager.get_function()
        function.set('rounding', event['new'])
        self.logger.write(self.logger.new_message('Prebieha prepočítavanie funkcie...'), timer=True)
        self.function_manager.update_plot(zero_points=True, extremes=True, inflex_points=True, monotonic=True, concave=True)
        self.logger.write(self.logger.new_message('zaokrúhlenie hodnôt', desatinné_miesta=event['new']), main=True, mini=True)
        self._add_zero_points_info(function, refinement_support=True)
        self._add_extremes_info(function, refinement_support=True)
        self._add_inflex_points_info(function, refinement_support=True)
        self._add_analysis_info(function, refinement_support=True)

    def _changed_extremes(self, event) -> None:
        """
        Event handler that turns plotting extremes on or off
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        if choice:
            function.set('extremes_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set('extremes_visible', choice)
        self.function_manager.update_plot()
        self._add_extremes_info(function)

    def _changed_color_extremes(self, event) -> None:
        """
        Event handler that changes color of extremes
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('extremes_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('extrémy', farba=choice), main=True, mini=True)

    def _changed_inflex_points(self, event) -> None:
        """
        Event handler that turns plotting inflex points on or off
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        if choice:
            function.set('inflex_points_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set('inflex_points_visible', choice)
        self.function_manager.update_plot()
        self._add_inflex_points_info(function)

    def _changed_color_inflex_points(self, event) -> None:
        """
        Event handler that changes color of inflex points
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('inflex_points_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('inflexné body', farba=choice), main=True, mini=True)

    def _changed_increasing(self, event) -> None:
        """
        Event handler that turns plotting increasing monotonic interval on or off
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        if choice:
            function.set('increasing_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set('increasing_visible', choice)
        self.function_manager.update_plot()
        self._add_analysis_info(function, op='increasing')

    def _changed_color_increasing(self, event) -> None:
        """
        Event handler that changes color of increasing monotonic interval
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('increasing_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('rastúca', farba=choice), main=True, mini=True)

    def _changed_decreasing(self, event) -> None:
        """
        Event handler that turns plotting decreasing monotonic interval on or off
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        if choice:
            function.set('decreasing_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set('decreasing_visible', choice)
        self.function_manager.update_plot()
        self._add_analysis_info(function, op='decreasing')

    def _changed_color_decreasing(self, event) -> None:
        """
        Event handler that changes color of decreasing monotonic interval
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('decreasing_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('klesajúca', farba=choice), main=True, mini=True)

    def _changed_concave_up(self, event) -> None:
        """
        Event handler that turns plotting concave interval on or off
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        if choice:
            function.set('concave_up_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set('concave_up_visible', choice)
        self.function_manager.update_plot()
        self._add_analysis_info(function, op='concave_up')

    def _changed_color_concave_up(self, event) -> None:
        """
        Event handler that changes color of concave up interval
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('concave_up_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('konvexná', farba=choice), main=True, mini=True)

    def _changed_concave_down(self, event) -> None:
        """
        Event handler that turns plotting concave interval on or off
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        if choice:
            function.set('concave_down_zorder', function.get_zorder_sum() + 1)
            function.update_zorder_sum()
        function.set('concave_down_visible', choice)
        self.function_manager.update_plot()
        self._add_analysis_info(function, op='concave_down')

    def _changed_color_concave_down(self, event) -> None:
        """
        Event handler that changes color of concave interval
        :param event: A data structure which saves user input information
        :return:
        """
        choice = event['new']
        function = self.function_manager.get_function()
        function.set('concave_down_color', choice)
        self.function_manager.update_plot()
        self.logger.write(self.logger.new_message('konkávna', farba=choice), main=True, mini=True)

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
