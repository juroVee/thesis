
class Observer:

    def __init__(self, board):
        self.plot = board.get_plot_object()
        self.logger = board.get_logger_object()
        self.gui_manager = board.get_gui_manager()
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
            function.set_grid(choice)
        self.plot.update()
        self.logger.write('Grid visible' if choice else 'Grid hidden')

    def _changed_derivative1(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        for function in self.function_manager.get_all():
            if choice:
                function.add_derivative(1)
            else:
                function.remove_derivative(1)
        self.plot.update()
        self.logger.write('Plotting 1. derivative' if choice else '1. derivative plot removed')

    def _changed_derivative2(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        for function in self.function_manager.get_all():
            if choice:
                function.add_derivative(2)
            else:
                function.remove_derivative(2)
        self.plot.update()
        self.logger.write('Plotting 2. derivative' if choice else '2. derivative plot removed')

    def _changed_derivative3(self, b) -> None:
        self.plot.updated = True
        choice = True if b['new'] == 'true' else False
        for function in self.function_manager.get_all():
            if choice:
                function.add_derivative(3)
            else:
                function.remove_derivative(3)
        self.plot.update()
        self.logger.write('Plotting 3. derivative' if choice else '3. derivative plot removed')

    def _changed_color_main(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        for function in self.function_manager.get_all():
            function.set_color(choice)
        self.plot.update()
        self.logger.write(f'Color of main function changed to {choice}')

    def _changed_color_derivative1(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        for function in self.function_manager.get_all():
            function.set_derivative_color(1, choice)
        self.plot.update()
        self.logger.write(f'Color of 1. derivative changed to {choice}')

    def _changed_color_derivative2(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        for function in self.function_manager.get_all():
            function.set_derivative_color(2, choice)
        self.plot.update()
        self.logger.write(f'Color of 2. derivative changed to {choice}')

    def _changed_color_derivative3(self, b) -> None:
        self.plot.updated = True
        choice = b['new']
        for function in self.function_manager.get_all():
            function.set_derivative_color(3, choice)
        self.plot.update()
        self.logger.write(f'Color of 3. derivative changed to {choice}')

    def _changed_refinement(self, b) -> None:
        self.plot.updated = True
        options = {'original':0, '10x':1, '100x':2, '1000x':3, '10000x':4}
        choice = options[b['new']]
        for function in self.function_manager.get_all():
            function.set_refinement(choice)
        self.plot.update()
        self.logger.write(f'Refinement set to {b["new"]} of it\'s original')

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