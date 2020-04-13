from queue import Queue

import ipywidgets as w
import matplotlib.pyplot as plt
from IPython.display import clear_output, display

from .function import Function, DefaultFunction, UserFunction
from .computations import ComputationsHandler
from ...config import config


class FunctionManager:

    def __init__(self, user_parameters):
        self._init_plot()
        self._init_structures()
        self._init_current_function(user_parameters)
        self.updates = 0

    def __getitem__(self, function_name: str):
        return self.functions[function_name]

    def _init_plot(self):
        self.output = w.Output()
        plt.ioff()
        width, height = config['plot_parameters']['width'], config['plot_parameters']['height']
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(width, height)

    def _init_structures(self):
        self.functions = {}
        self.warnings = Queue()

    def _init_current_function(self, user_parameters) -> None:
        if bool(user_parameters):
            current = self.functions['user function'] = UserFunction(user_parameters)
        else:
            parameters = config['main_function']['default']
            current = self.functions[parameters['name']] = DefaultFunction(parameters['name'], parameters)
        self.current_function = current

    def get_all(self) -> dict.values:
        return self.functions.values()

    def get_current(self) -> Function:
        return self.current_function

    def set_current(self, name) -> None:
        if name in self.functions:
            self.current_function = self.functions[name]
        else:
            parameters = config['main_function']['default']
            self.current_function = self.functions[parameters['name']] = DefaultFunction(parameters['name'], parameters)

    def add_warnings(self, warnings):
        if warnings is not None:
            if len(warnings) > 0:
                for warning in warnings:
                    self.warnings.put(warning)

    def get_warnings(self):
        return self.warnings

    def update_plot(self, **kwargs) -> None:
        if len(kwargs) > 0:
            calculator = ComputationsHandler(function=self.get_current())
            for arg, value in kwargs.items():
                if value:
                    warnings = getattr(calculator, arg)()
                    self.add_warnings(warnings)
        # important!
        if self.updates > 0:
            plt.close('all')

        current_function = self.get_current()
        current_function.plot(self.ax)
        self.updates += 1
        with self.output:
            clear_output(wait=True)
            display(self.ax.figure)
        plt.ion()

    def get_plot_widget(self):
        return self.output
