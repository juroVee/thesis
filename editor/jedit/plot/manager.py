# external modules
import matplotlib.pyplot as plt
import ipywidgets as w
from IPython.display import clear_output
import queue

# project-level modules
from ..config import config
from .calculations import calculate_main_function, calculate_derivatives, calculate_zero_points
from .function import Function, DefaultFunction, UserFunction

class Manager:

    output = w.Output()

    def __init__(self, user_params):
        self.plot_updated = False
        self.functions = {}
        self.warnings = queue.Queue()
        self.names_mapping = {params['name']: key for key, params in config['default_functions'].items()}
        if bool(user_params):
            self.current_function = self.functions['user function'] = UserFunction(user_params)
        else:
            default_function = config['main_function']['default']
            parameters = config['default_functions'][default_function]
            self.current_function = self.functions[parameters['name']] = DefaultFunction(parameters['name'], parameters)

    def __getitem__(self, function_name: str):
        return self.functions[function_name]

    def apply_configuration(self, configuration):
        for parameter, value in configuration.items():
            if parameter == 'refinement':
                self.current_function.set_refinement(value)
            else:
                self.current_function.set_parameter(parameter, value)

    def get_all(self) -> dict.values:
        return self.functions.values()

    def get_current(self) -> Function:
        return self.current_function

    def set_current(self, name) -> None:
        if name in self.functions:
            self.current_function = self.functions[name]
        else:
            parameters = config['default_functions'][self.names_mapping[name]]
            self.current_function = self.functions[parameters['name']] = DefaultFunction(parameters['name'], parameters)

    def set_plot_updated(self, value):
        self.plot_updated = value

    def has_user_function(self) -> bool:
        return 'user function' in self.functions.keys()

    def add_warnings(self, message, warnings):
        if len(warnings) > 0:
            for warning in warnings:
                self.warnings.put((message, warning))

    def get_warnings(self, logger):
        while not self.warnings.empty():
            warning_type, warning = self.warnings.get()
            logger.write_warning(f'{warning_type}: {warning.message}')

    def update_plot(self, full=False) -> None:
        if full:
            calculate_main_function(self.get_current())
            calculate_derivatives(self.get_current())
            _, warnings = calculate_zero_points(self.get_current())
            self.add_warnings(f'Calculating zero points ({self.get_current().get_parameter("name")}) warning', warnings)
        with self.output:
            clear_output()
            if self.plot_updated:
                plt.close('all') # very important, possible memory exceeding
            self.get_current().plot()

    def get_plot_widget(self):
        return self.output