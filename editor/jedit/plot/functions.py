# external modules
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# project-level modules
from ..config import config
from ..util import transform_title

# package-level modules
from .maux import init_subplot, smart_ticklabel
from .calculations import Calculator


class Function:

    def __init__(self, X, Y, f, name, latex):
        self.parameters = {}
        self._init_function_details(X, Y, f, name, latex)
        self._init_plot_parameters()
        self._init_derivatives()
        self._init_zero_points()
        self._init_refinement()

    def _init_function_details(self, X, Y, formula, name, latex_representation):
        self.set_parameter('x_values', X)
        self.set_parameter('original_x_values', X)
        self.set_parameter('y_values', Y)
        self.set_parameter('formula', formula)
        self.set_parameter('name', name)
        self.set_parameter('latex', latex_representation)
        self.set_parameter('lines_count', len(list(X)))

    def _init_plot_parameters(self):
        self.set_parameter('grid', True if config['default_plot_params']['grid'] == 'yes' else False)
        self.set_parameter('main_function_color', config['default_colors']['main_function'])
        for n in range(1, config['default_plot_params']['max_derivative'] + 1):
            self.set_parameter('derivative_color' + str(n), config['default_colors']['derivatives'][n-1])

    def _init_derivatives(self):
        self.recalculate_derivatives()
        for n in range(1, config['default_plot_params']['max_derivative'] + 1):
            self.set_parameter('active_derivative' + str(n), False)

    def _init_zero_points(self):
        self.set_parameter('zero_points_method', 'none')
        self.set_parameter('zero_points_values', set())
        self.set_parameter('zero_points_color', config['default_colors']['zero_points'])

    def _init_refinement(self):
        self.set_parameter('refinement', 0)

    def recalculate_main_function(self):
        function = self.get_parameter('formula')
        self.set_parameter('y_values', [function(X) for X in self.get_parameter('x_values')])
        self.set_parameter('lines', [Line2D(X, Y) for X, Y in zip(self.get_parameter('x_values'), self.get_parameter('y_values'))])

    def recalculate_derivatives(self):
        calculator = Calculator(self.get_parameter('formula'))
        x_values, y_values = self.get_parameter('x_values'), self.get_parameter('y_values')
        derivatives = {}
        for X, Y in zip(x_values, y_values):
            for n in range(1, config['default_plot_params']['max_derivative'] + 1):
                _, dydx = calculator.derive(X, n)
                derivatives[n] = (X, dydx)
        self.set_parameter('derivatives', derivatives)

    def plot(self) -> None:
        # # DEBUG ONLY -> DELETE
        # for xval in self.get_parameter('x_values'):
        #     print(f'(DEBUG) Refinement: {self.get_parameter("refinement")} Intervals: {len(xval)-1} Values: {len(xval)}')
        fig, ax = plt.subplots()
        fig.set_size_inches(6, 5)

        painter = FunctionPainter(self, ax)
        painter.plot_main_function()
        painter.plot_derivative()
        painter.plot_zero_points()
        painter.plot_title()

        fig.show()

    def set_parameter(self, name, value):
        self.parameters[name] = value

    def get_parameter(self, parameter):
        return self.parameters[parameter]

    def set_refinement(self, value=0) -> None:
        self.set_parameter('refinement', value)
        if value == 0:
            self.set_parameter('x_values', self.get_parameter('original_x_values'))
            return
        new_x_values = []
        for xval in self.get_parameter('original_x_values'):
            minima, maxima = min(xval), max(xval)
            intervals = len(xval) - 1
            new_intervals = intervals * self.get_parameter('refinement')
            new_x_values.append(np.linspace(minima, maxima, new_intervals + 1))
        self.set_parameter('x_values', new_x_values)
        
class UserFunction(Function):
    
    def __init__(self, user_data=None):
        self.user_data = user_data
        fig, ax, f = user_data['figure'], user_data['axis'], user_data['f']
        X = [xvals for xvals in user_data['xvals']]
        Y = [f(xvals) for xvals in X]
        super().__init__(X, Y, f, name='user function', latex=transform_title(ax.get_title()))
        self._init_params(ax)
        
    def _init_params(self, ax):
        self.set_parameter('title', ax.get_title())
        self.set_parameter('aspect', ax.get_aspect())
        self.set_parameter('xticks', ax.get_xticks())
        self.set_parameter('yticks', ax.get_yticks())
        if ax.get_xticklabels()[0].get_text() != '':
            self.set_parameter('xticklabels', ax.get_xticklabels())
        if ax.get_yticklabels()[0].get_text() != '':
            self.set_parameter('yticklabels', ax.get_yticklabels())
        self.set_parameter('xlim', ax.get_xlim())
        self.set_parameter('ylim', ax.get_ylim())
        lines = [line for line in ax.get_lines() if line.get_xdata() != [] and line.get_ydata() != []]
        self.set_parameter('lines', lines)


class DefaultFunction(Function):

    def __init__(self, name='undefined', config_data=None):
        function = eval(config_data['formula'])
        X = eval(config_data['linspace'])
        latex = eval(config_data['latex'])
        super().__init__([X], [function(X)], function, name, latex)
        self.set_parameter('lines', [Line2D(X, function(X))])
        self.set_parameter('title', latex)
        self.set_parameter('aspect', 'equal' if config['default_plot_params']['aspect'] == 'equal' else 'auto')
        if 'xticks_data' in config_data:
            self.set_parameter('xticks', eval(config_data['xticks_data']['xticks']))
            self.set_parameter('xticklabels', eval(config_data['xticks_data']['xticklabels']))
        

class FunctionManager:

    def __init__(self, user_data: dict):
        self.functions = {}
        default_functions = config['default_functions']
        for _, parameters in default_functions.items():
            name = parameters['name']
            self.functions[name] = DefaultFunction(name, parameters)
        default_function = config['default_plot_params']['function']
        self.current_function = self.functions[config['default_functions'][default_function]['name']]
        if user_data is not None:
            self.current_function = self.functions['user function'] = UserFunction(user_data)

    def __getitem__(self, function_name: str):
        return self.functions[function_name]

    def apply_configuration(self, configuration):
        for parameter, value in configuration.items():
            if parameter == 'refinement':
                self.current_function.set_refinement(value)
                self.current_function.recalculate_main_function()
                self.current_function.recalculate_derivatives()
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


class FunctionPainter:

    def __init__(self, function, axes):
        self.function, self.ax = function, axes

    def plot_main_function(self):
        lines_count = self.function.get_parameter('lines_count')
        for line in self.function.get_parameter('lines'):
            X, Y = line.get_xdata(), line.get_ydata()
            init_subplot(self.ax)
            for param in self.function.parameters:
                try:
                    method = getattr(self.ax, 'set_' + param)
                    method(self.function.parameters[param])
                except AttributeError:
                    pass
            self.ax.grid(self.function.get_parameter('grid'))
            self.ax.plot(X, Y,
                    color=self.function.get_parameter('main_function_color') if line.get_linestyle() == '-' else line.get_color(),
                    label=self.function.get_parameter('latex') if lines_count == 1 else '',
                    linestyle=line.get_linestyle(),
                    linewidth=line.get_linewidth())

    def plot_derivative(self):
        lines_count = self.function.get_parameter('lines_count')
        for n in range(1, config['default_plot_params']['max_derivative'] + 1):
            if self.function.get_parameter('active_derivative' + str(n)):
                X, dydx = self.function.get_parameter('derivatives').get(n)
                quotes = n * "'"
                color = self.function.get_parameter('derivative_color' + str(n))
                self.ax.plot(X, dydx, color=color, label=fr"f{quotes}(x)" if lines_count == 1 else '')

    def plot_zero_points(self):
        if self.function.get_parameter('zero_points_method') != 'none':
            calculator = Calculator(self.function.get_parameter('formula'))
            x_values, y_values = self.function.get_parameter('x_values'), self.function.get_parameter('y_values')
            zero_points = set()
            for X, Y in zip(x_values, y_values):
                zero_points.update(list(calculator.zero_points(X, method=self.function.get_parameter('zero_points_method'))))
            self.function.set_parameter('zero_points_values', zero_points)
            for x in self.function.get_parameter('zero_points_values'):
                self.ax.plot(x, 0, 'ko', c=self.function.get_parameter('zero_points_color'))

    def plot_title(self):
        self.ax.set_title(self.function.get_parameter('latex'))