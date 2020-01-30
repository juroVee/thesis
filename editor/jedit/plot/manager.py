# project-level modules
from ..config import config

from .function import Function, DefaultFunction, UserFunction

class Manager:

    def __init__(self, user_params):
        self.functions = {}
        default_functions = config['default_functions']
        for _, parameters in default_functions.items():
            name = parameters['name']
            self.functions[name] = DefaultFunction(name, parameters)
        default_function = config['main_function']['default']
        self.current_function = self.functions[config['default_functions'][default_function]['name']]
        if bool(user_params):
            self.current_function = self.functions['user function'] = UserFunction(user_params)

    def create_function(self, user_parameters):
        ...

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

    def has_user_function(self) -> bool:
        return 'user function' in self.functions.keys()