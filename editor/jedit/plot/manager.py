# external modules
import matplotlib.pyplot as plt
import ipywidgets as w
from IPython.display import clear_output

# project-level modules
from ..config import config

from .function import Function, DefaultFunction, UserFunction

class Manager:

    output = w.Output()

    def __init__(self, user_params):
        self.plot_updated = False
        self.functions = {}
        default_functions = config['default_functions']
        for _, parameters in default_functions.items():
            name = parameters['name']
            self.functions[name] = DefaultFunction(name, parameters)
        default_function = config['main_function']['default']
        self.current_function = self.functions[config['default_functions'][default_function]['name']]
        if bool(user_params):
            self.current_function = self.functions['user function'] = UserFunction(user_params)

    def __getitem__(self, function_name: str):
        return self.functions[function_name]

    def apply_configuration(self, configuration):
        calculator = self.current_function.get_calculator()
        for parameter, value in configuration.items():
            if parameter == 'refinement':
                self.current_function.set_refinement(value)
                calculator.calculate_main_function()
                calculator.calculate_derivatives()
            else:
                self.current_function.set_parameter(parameter, value)

    def get_all(self) -> dict.values:
        return self.functions.values()

    def get_current(self) -> Function:
        return self.current_function

    def set_current(self, function: Function) -> None:
        self.current_function = function

    def set_plot_updated(self, value):
        self.plot_updated = value

    def has_user_function(self) -> bool:
        return 'user function' in self.functions.keys()

    def update_plot(self) -> None:
        with self.output:
            clear_output()
            if self.plot_updated:
                plt.close('all') # very important, possible memory exceeding
            self.get_current().plot()

    def get_plot_widget(self):
        return self.output