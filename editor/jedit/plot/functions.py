# external modules
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from collections import defaultdict

# project-level modules
from ..config import config
from ..util import transform_title

# package-level modules
from .maux import init_subplot, smart_ticklabel
from .calculations import DerivativeCalculator, ZeroPointsCalculator


class Function:

    def __init__(self, f, X, name, latex, user_derivatives=None, asymptotes=None):
        self.parameters = {}
        self._init_function_details(X, f, name, latex, user_derivatives, asymptotes)
        self._init_plot_parameters()
        self._init_derivatives()
        self._init_zero_points()
        self._init_refinement()

    def _init_function_details(self, X, formula, name, latex_representation, user_derivatives, asymptotes):
        self.set_parameter('x_values', X)
        self.set_parameter('original_x_values', X)
        self.set_parameter('formula', formula)
        self.set_parameter('name', name)
        self.set_parameter('latex', latex_representation)
        self.set_parameter('user_derivatives', [] if user_derivatives is None else user_derivatives)
        self.set_parameter('asymptotes', [] if asymptotes is None else asymptotes)
        self.set_parameter('lines_count', len(list(X)))
        self.recalculate_main_function()

    def _init_plot_parameters(self):
        self.set_parameter('grid', True if config['plot_parameters']['grid'] == 'yes' else False)
        self.set_parameter('main_function_color', config['main_function']['color'])
        for n in range(1, config['derivative']['max_derivative'] + 1):
            self.set_parameter('derivative_color' + str(n), config['derivative']['colors'][n - 1])

    def _init_derivatives(self):
        self.recalculate_derivatives()
        for n in range(1, config['derivative']['max_derivative'] + 1):
            self.set_parameter('active_derivative' + str(n), False)

    def _init_zero_points(self):
        self.set_parameter('zero_points_method', 'none')
        self.set_parameter('zero_points_values', set())
        self.set_parameter('zero_points_color', config['zero_points']['color'])

    def _init_refinement(self):
        self.set_parameter('refinement', 1)

    def recalculate_main_function(self):
        function = self.get_parameter('formula')
        self.set_parameter('y_values', [function(X) for X in self.get_parameter('x_values')])
        self.set_parameter('lines', [Line2D(X, Y) for X, Y in
                                     zip(self.get_parameter('x_values'), self.get_parameter('y_values'))])

    def recalculate_derivatives(self):
        calculator = DerivativeCalculator(self.get_parameter('formula'))
        x_values, y_values = self.get_parameter('x_values'), self.get_parameter('y_values')
        derivatives = {}
        for X, Y in zip(x_values, y_values):
            for n in range(1, config['derivative']['max_derivative'] + 1):
                if len(self.get_parameter('user_derivatives')) >= n:
                    d = self.get_parameter('user_derivatives')[n - 1]
                    derivatives[n] = (X, d(X))
                else:
                    _, dydx = calculator.derive(X, n)
                    derivatives[n] = (X, dydx)
        self.set_parameter('derivatives', derivatives)

    def recalculate_zero_points_derivative_signs(self):
        if self.get_parameter('zero_points_method') != 'none':
            calculator_d = DerivativeCalculator(self.get_parameter('formula'))
            zero_points_derivatives_signs = defaultdict(dict)
            for zero_point in self.get_parameter('zero_points_values'):
                for n in range(1, config['derivative']['max_derivative'] + 1):
                    _, d = calculator_d.derive(zero_point, n)
                    zero_points_derivatives_signs[zero_point][n] = '-' if d < 0 else '+' if d > 0 else '0'
            self.set_parameter('zero_points_derivatives_signs', zero_points_derivatives_signs)


    def plot(self) -> None:
        # # DEBUG ONLY -> DELETE
        # for xval in self.get_parameter('x_values'):
        #     print(f'(DEBUG) Refinement: {self.get_parameter("refinement")} Intervals: {len(xval)-1} Values: {len(xval)}')

        width, height = config['plot_parameters']['width'], config['plot_parameters']['height']

        fig, ax = plt.subplots()
        fig.set_size_inches(width, height)

        painter = FunctionPainter(self, ax)
        painter.plot_main_function()
        painter.plot_asymptotes()
        painter.plot_derivative()
        painter.plot_zero_points()
        painter.plot_title()

        fig.show()

    def set_parameter(self, name, value):
        self.parameters[name] = value

    def get_parameter(self, parameter):
        return self.parameters.get(parameter, None)

    def set_refinement(self, value=1) -> None:
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

    def __init__(self, user_params):
        user_params = self._prepare_user_params(user_params)
        ax, X, f = user_params['ax'], user_params['X'], user_params['f']
        user_derivatives = user_params.get('derivatives', None)
        asymptotes = user_params.get('asymptotes', None)
        super().__init__(f, X, name='user function',
                         latex=transform_title(ax.get_title()),
                         user_derivatives=user_derivatives,
                         asymptotes=asymptotes)
        self._init_params(ax, asymptotes)

    def _prepare_user_params(self, user_params):
        ax = user_params['ax']
        if user_params.get('X', None) is None:
            lines = [line.get_xdata() for line in ax.get_lines() if line.get_xdata() != []]
            if 'asymptotes' in user_params:
                user_lines_number = len(user_params['X'])
                user_params['X'] = lines[:user_lines_number]

        return user_params

    def _init_params(self, ax, asymptotes=None):
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
        if asymptotes is not None:
            user_lines_number = len(self.get_parameter('x_values'))
            self.set_parameter('lines', lines[:user_lines_number])
            self.set_parameter('asymptotes', lines[user_lines_number:])
            return
        self.set_parameter('lines', lines)
        self.set_parameter('asymptotes', [])


class DefaultFunction(Function):

    def __init__(self, name='undefined', config_data=None):
        function = eval(config_data['formula'])
        X = eval(config_data['linspace'])
        latex = eval(config_data['latex'])
        super().__init__(function, [X], name, latex, user_derivatives=None, asymptotes=None)
        self.set_parameter('lines', [Line2D(X, function(X))])
        self.set_parameter('title', latex)
        self.set_parameter('aspect', 'equal' if config['plot_parameters']['aspect'] == 'equal' else 'auto')
        if 'xticks_data' in config_data:
            self.set_parameter('xticks', eval(config_data['xticks_data']['xticks']))
            self.set_parameter('xticklabels', eval(config_data['xticks_data']['xticklabels']))


class FunctionManager:

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

    def __getitem__(self, function_name: str):
        return self.functions[function_name]

    def apply_configuration(self, configuration):
        for parameter, value in configuration.items():
            if parameter == 'refinement':
                self.current_function.set_refinement(value)
                self.current_function.recalculate_main_function()
                self.current_function.recalculate_derivatives()
                self.current_function.recalculate_zero_points_derivative_signs()
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
                         color=self.function.get_parameter('main_function_color'),
                         linestyle=config['main_function']['linestyle'],
                         linewidth=config['main_function']['linewidth'],
                         zorder=3)

    def plot_asymptotes(self):
        for line in self.function.get_parameter('asymptotes'):
            X, Y = line.get_xdata(), line.get_ydata()
            linestyle = config['asymptote']['linestyle']
            linewidth = config['asymptote']['linewidth']
            color = config['asymptote']['color']
            self.ax.plot(X, Y,
                         color=color,
                         linestyle=linestyle,
                         linewidth=linewidth,
                         zorder=1)

    def plot_derivative(self):
        for n in range(1, len(self.function.get_parameter('derivatives')) + 1):
            if self.function.get_parameter('active_derivative' + str(n)):
                X, dydx = self.function.get_parameter('derivatives').get(n)
                color = self.function.get_parameter('derivative_color' + str(n))
                linestyle = config['derivative']['linestyle']
                linewidth = config['derivative']['linewidth']
                self.ax.plot(X, dydx,
                             color=color,
                             linestyle=linestyle,
                             linewidth=linewidth,
                             zorder=2)

    def plot_zero_points(self):
        if self.function.get_parameter('zero_points_method') != 'none':
            calculator = ZeroPointsCalculator(self.function.get_parameter('formula'))
            x_values, y_values = self.function.get_parameter('x_values'), self.function.get_parameter('y_values')
            method = self.function.get_parameter('zero_points_method')
            zero_points = set()
            for X, Y in zip(x_values, y_values):
                calculated = calculator.zero_points(X, method=method)
                zero_points.update(calculated)
            self.function.set_parameter('zero_points_values', zero_points)
            markersize = config['zero_points']['markersize']
            for x in self.function.get_parameter('zero_points_values'):
                self.ax.plot(x, 0, 'o', c=self.function.get_parameter('zero_points_color'), markersize=markersize, zorder=4)

    def plot_title(self):
        self.ax.set_title(self.function.get_parameter('latex'), y=1.06)