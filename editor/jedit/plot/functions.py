# external modules
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# project-level modules
from ..settings import DEFAULT_FUNCTIONS, DEFAULT_FUNCTION_TO_SHOW, DERIV_COLORS
from ..util import transform_title
from ..calculations import Calculator

# package-level modules
from .painter import Painter


class Function:

    def __init__(self, X, Y, f, name, latex):
        self.x_values, self.y_values = X, Y
        self.f, self.name, self.latex = f, name, latex

        self.calculator = Calculator(f)

        # plot params shared
        self.grid = False
        self.color = 'C0'
        self.derivative_colors = DERIV_COLORS
        self.parameters = {'derivatives':set()}

        self.original_x_values = X
        self.refinement = 0
        self.zero_points = 'none'
        self.zero_points_values = []
        self.zero_points_color = '#000000'

    def __repr__(self):
        return f'Function(name={self.name})'

    def plot(self) -> None:
        # DEBUG ONLY -> DELETE
        # for xval in self.x_values:
        #     print(f'(DEBUG) Refinement: {self.refinement} Intervals: {len(xval)-1} Values: {len(xval)}')
        fig, ax = plt.subplots()
        fig.set_size_inches(6, 5)

        painter = Painter(self, ax)
        painter.plot_main_function()
        painter.plot_derivative()
        painter.plot_zero_points()
        painter.plot_title()

        fig.show()

    def get_calculator(self):
        return self.calculator

    def set_parameter(self, name, value):
        self.parameters[name] = value

    def add_derivative(self, n):
        self.parameters['derivatives'].add(n)

    def remove_derivative(self, n):
        self.parameters['derivatives'].discard(n)

    def set_grid(self, value=False) -> None:
        self.grid = value

    def set_color(self, value='C0') -> None:
        self.color = value

    def set_derivative_color(self, n, value='C0'):
        self.derivative_colors[n] = value

    def get_derivative_color(self, n):
        return self.derivative_colors[n]

    def set_refinement(self, value=0) -> None:
        self.refinement = value
        new_x_values = []
        for xval in self.original_x_values:
            minima, maxima = min(xval), max(xval)
            intervals = len(xval) - 1
            new_intervals = intervals* (10 ** self.refinement)
            new_x_values.append(np.linspace(minima, maxima, new_intervals + 1))
        self.x_values = new_x_values

    def set_zero_points(self, value):
        self.zero_points = value

    def set_zero_points_color(self, value):
        self.zero_points_color = value

    def get_zero_points(self):
        return self.zero_points_values

    def get_name(self) -> str:
        return self.name

    def get_latex(self) -> str:
        return self.latex


class FunctionManager:

    def __init__(self, user_data: dict):
        self.functions = {}
        self._load_default_functions()
        self.current_function = self.functions[DEFAULT_FUNCTION_TO_SHOW]
        if user_data is not None:
            self._load_user_function(user_data)

    def _load_default_functions(self) -> None:
        for name, data in DEFAULT_FUNCTIONS.items():
            function, X, latex = data['f'], data['linspace'], data['latex']
            func = Function([X], [function(X)], function, name, latex)
            lines = [Line2D(X, function(X))]
            func.set_parameter('lines', lines)
            func.set_parameter('title', latex)
            func.set_parameter('aspect', 'auto')
            if 'xticks_data' in data.keys():
                func.set_parameter('xticks', data['xticks_data']['xticks'])
                func.set_parameter('xticklabels', data['xticks_data']['xticklabels'])
            self.functions[name] = func

    def _load_user_function(self, user_data: dict) -> None:
        fig, ax, f = user_data['figure'], user_data['axis'], user_data['f']
        X = [xvals for xvals in user_data['xvals']]
        Y = [f(xvals) for xvals in X]
        self.current_function = self.functions['user function'] = Function(
            X = X,
            Y = Y,
            f=f,
            name='user function',
            latex=transform_title(ax.get_title())
        )
        self.current_function.set_parameter('title', ax.get_title())
        self.current_function.set_parameter('aspect', ax.get_aspect())
        self.current_function.set_parameter('xticks', ax.get_xticks())
        self.current_function.set_parameter('yticks', ax.get_yticks())
        if ax.get_xticklabels()[0].get_text() != '':
            self.current_function.set_parameter('xticklabels', ax.get_xticklabels())
        if ax.get_yticklabels()[0].get_text() != '':
            self.current_function.set_parameter('yticklabels', ax.get_yticklabels())
        self.current_function.set_parameter('xlim', ax.get_xlim())
        self.current_function.set_parameter('ylim', ax.get_ylim())
        lines = [line for line in ax.get_lines() if line.get_xdata() != [] and line.get_ydata() != []]
        self.current_function.set_parameter('lines', lines)

    def __getitem__(self, function_name: str):
        return self.functions[function_name]

    def __repr__(self):
        return 'FunctionManager(\n\t' + '\n\t'.join(self.functions) + '\n)'

    def get_all(self) -> dict.values:
        return self.functions.values()

    def get_current(self) -> Function:
        return self.current_function

    def set_current(self, function: Function) -> None:
        self.current_function = function

    def has_user_function(self) -> bool:
        return 'user function' in self.functions.keys()