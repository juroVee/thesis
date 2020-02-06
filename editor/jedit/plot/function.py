# external modules
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# project-level modules
from ..config import config
from ..util import transform_title

# package-level modules
from .maux import init_subplot, smart_ticklabel
from .painter import Painter


class Function:

    def __init__(self, f, X, name, latex, user_derivatives=None, asymptotes=None):
        self.parameters = {}
        self._init_function_details(X, f, name, latex, user_derivatives, asymptotes)
        self._init_plot_parameters()
        self._init_derivatives()
        self._init_zero_points()
        self._init_refinement()

    def _init_function_details(self, X, f, name, latex_representation, user_derivatives, asymptotes):
        self.set_parameter('x_values', X)
        self.set_parameter('original_x_values', X)
        self.set_parameter('f', f)
        self.set_parameter('name', name)
        self.set_parameter('latex', latex_representation)
        self.set_parameter('user_derivatives', [] if user_derivatives is None else user_derivatives)
        self.set_parameter('asymptotes', [] if asymptotes is None else asymptotes)
        self.set_parameter('lines_count', len(list(X)))

    def _init_plot_parameters(self):
        self.set_parameter('grid', True if config['plot_parameters']['grid'] == 'yes' else False)
        self.set_parameter('main_function_color', config['main_function']['color'])
        for n in range(1, config['derivative']['max_derivative'] + 1):
            self.set_parameter('derivative_color' + str(n), config['derivative']['colors'][n - 1])

    def _init_derivatives(self):
        for n in range(1, config['derivative']['max_derivative'] + 1):
            self.set_parameter('active_derivative' + str(n), False)

    def _init_zero_points(self):
        self.set_parameter('zero_points_visible', False)
        if len(self.get_parameter('user_derivatives')) > 0:
            self.set_parameter('zero_points_method', 'Newton')
        else:
            self.set_parameter('zero_points_method', 'Secant')
        self.set_parameter('zero_points_color', config['zero_points']['color'])
        self.set_parameter('zero_points_iterations', config['zero_points']['iterations'])

    def _init_refinement(self):
        self.set_parameter('refinement', 1)

    def plot(self) -> None:
        # # DEBUG ONLY -> DELETE
        # for xval in self.get_parameter('x_values'):
        #     print(f'(DEBUG) Refinement: {self.get_parameter("refinement")} Intervals: {len(xval)-1} Values: {len(xval)}')

        width, height = config['plot_parameters']['width'], config['plot_parameters']['height']

        fig, ax = plt.subplots()
        fig.set_size_inches(width, height)

        painter = Painter(self, ax)
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
        user_derivatives = user_params.get('primes', None)
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
        for param in ['title', 'aspect', 'xticks', 'yticks', 'xlim', 'ylim']:
            if hasattr(ax, f'get_{param}'):
                method = getattr(ax, f'get_{param}')
                self.set_parameter(param, method())
        if ax.get_xticklabels()[0].get_text() != '':
            self.set_parameter('xticklabels', ax.get_xticklabels())
        if ax.get_yticklabels()[0].get_text() != '':
            self.set_parameter('yticklabels', ax.get_yticklabels())
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
        derivatives = [eval(derivative) for derivative in config_data.get('derivatives', [])]
        super().__init__(function, [X], name, latex, user_derivatives=derivatives, asymptotes=None)
        self.set_parameter('lines', [Line2D(X, function(X))])
        self.set_parameter('title', latex)
        self.set_parameter('aspect', 'equal' if config['plot_parameters']['aspect'] == 'equal' else 'auto')
        if 'xticks_data' in config_data:
            self.set_parameter('xticks', eval(config_data['xticks_data']['xticks']))
            self.set_parameter('xticklabels', eval(config_data['xticks_data']['xticklabels']))