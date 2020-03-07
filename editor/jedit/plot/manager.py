# external modules
import matplotlib.pyplot as plt
import ipywidgets as w
from IPython.display import clear_output
from queue import Queue

# project-level modules
from ..config import config
from .calculations import Calculator
from .function import Function, DefaultFunction, UserFunction

class Manager:

    output = w.Output()

    def __init__(self, user_params):
        self.plot_updated = False
        self.functions = {}
        self.warnings = Queue()
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

    def add_warnings(self, message, triple):
        warnings, not_conv, zero_der = triple
        if len(warnings) > 0:
            for warning in warnings:
                self.warnings.put((message, warning, not_conv, zero_der))

    def get_warnings(self):
        return self.warnings

    def update_plot(self, **kwargs) -> None:
        calculator = Calculator(self.get_current())
        for arg, value in kwargs.items():
            if value:
                if arg in ('zero_points', 'extremes'):
                    _, triple = getattr(calculator, arg)()
                    self.add_warnings('Warning', triple)
                else:
                    getattr(calculator, arg)()
        with self.output:
            clear_output()
            if self.plot_updated:
                plt.close('all') # very important, possible memory exceeding
            self.get_current().plot()

    def get_plot_widget(self):
        return self.output