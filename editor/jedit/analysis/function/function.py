import numpy as np
from matplotlib.lines import Line2D

from ..plotting import Plotter
from ...config import config


class Function:
    """
    Class that serves as a container for all the useful information about particular user function
    """

    def __init__(self, f, X, name, user_derivatives=None, asymptotes=None):
        self.parameters = {}
        self.zorder_sum = 4
        self._init_function_details(X, f, name, user_derivatives, asymptotes)
        self._init_plot_parameters()
        self._init_derivatives()
        self._init_zero_points()
        for op in 'extremes', 'inflex_points', 'increasing', 'decreasing', 'concave_up', 'concave_down':
            self._init_analysis(op)
        self._init_refinements()

    def _init_function_details(self, X, f, name, user_derivatives, asymptotes):
        self.set('x_values', X)
        self.set('original_x_values', X)
        self.set('f', f)
        self.set('name', name)
        self.set('user_derivatives', user_derivatives)
        self.set('asymptotes', asymptotes)
        self.set('lines_count', len(list(X)))
        self.set('rounding', config['editor_settings']['round']['default'])

    def _init_plot_parameters(self):
        self.set('grid', True if config['plot_parameters']['grid'] == 'yes' else False)
        self.set('main_function_color', config['main_function']['color'])
        for n in range(1, config['derivative']['user_max'] + 1):
            self.set('derivative_color' + str(n), config['derivative']['colors'][n - 1])

    def _init_derivatives(self):
        for n in range(1, config['derivative']['user_max'] + 1):
            self.set('active_derivative' + str(n), False)

    def _init_zero_points(self):
        self.set('zero_points_visible', False)
        if len(self.get('user_derivatives')) == 1:
            self.set('zero_points_method', 'Newton')
        elif len(self.get('user_derivatives')) == 2:
            self.set('zero_points_method', 'Halley')
        else:
            self.set('zero_points_method', 'Secant')
        self.set('zero_points_color', config['zero_points']['color'])
        self.set('zero_points_iterations', config['zero_points']['iterations'])

    def _init_analysis(self, op='extremes'):
        self.set(f'{op}_visible', False)
        self.set(f'{op}_color', config[op]['color'])

    def _init_refinements(self):
        self.set('refinement_x', 1)
        self.set('refinement_y', 1)

    def set_refinement_x(self, value=1) -> None:
        self.set('refinement', value)
        if value == 0:
            self.set('x_values', self.get('original_x_values'))
            return
        f = self.get('f')
        new_x_values = []
        for X in self.get('original_x_values'):
            minima, maxima = min(X), max(X)
            intervals = len(X) - 1
            new_intervals = intervals * self.get('refinement')
            new_X = np.linspace(minima, maxima, new_intervals + 1)
            with np.errstate(divide='ignore', invalid='ignore'):
                new_x_values.append(new_X[~np.isnan(f(new_X))])
        self.set('x_values', new_x_values)

    def plot(self, ax) -> None:
        """
        Plots all the information about function if user selected as visible
        :param ax: matplotlib Axes object
        :return:
        """
        ax.clear()
        Plotter(self, ax).plot_all()

    def set(self, name, value) -> None:
        """
        Sets or changes function's parameter
        :param name: Name of the parameter
        :param value: Value of the parameter
        :return:
        """
        self.parameters[name] = value

    def get(self, parameter):
        """
        Gets parameter
        :param parameter: Parameter's name
        :return:
        """
        return self.parameters.get(parameter, None)

    def update_zorder_sum(self) -> None:
        """
        Increases plot objects count
        :return:
        """
        self.zorder_sum += 1

    def get_zorder_sum(self) -> int:
        """
        Gets plot objects count
        :return:
        """
        return self.zorder_sum


class UserFunction(Function):

    def __init__(self, user_params):
        user_params = self._prepare_user_params(user_params)
        ax, X, f = user_params['axes'], user_params['intervals'], user_params['function']
        user_derivatives = {i+1 : user_params.get('primes', [])[i] for i in range(len(user_params.get('primes', [])))}
        asymptotes = user_params.get('asymptotes', [])
        super().__init__(f, X, name='user function',
                         user_derivatives=user_derivatives,
                         asymptotes=asymptotes)
        self._init_params(ax, asymptotes)

    def _prepare_user_params(self, user_params):
        ax = user_params['axes']
        if user_params.get('X', None) is None:
            lines = [line.get_xdata() for line in ax.get_lines() if line.get_xdata() != []]
            if 'asymptotes' in user_params:
                user_lines_number = len(user_params['intervals'])
                user_params['intervals'] = lines[:user_lines_number]
        return user_params

    def _init_params(self, ax, asymptotes=None):
        for param in ['aspect', 'xticks', 'yticks', 'xlim', 'ylim']:
            if hasattr(ax, f'get_{param}'):
                method = getattr(ax, f'get_{param}')
                self.set(param, method())
        if ax.get_xticklabels()[0].get_text() != '':
            self.set('xticklabels', ax.get_xticklabels())
        if ax.get_yticklabels()[0].get_text() != '':
            self.set('yticklabels', ax.get_yticklabels())
        lines = [line for line in ax.get_lines() if line.get_xdata() != [] and line.get_ydata() != []]
        if asymptotes is not None:
            user_lines_number = len(self.get('x_values'))
            self.set('lines', lines[:user_lines_number])
            self.set('asymptotes', lines[user_lines_number:])
            return
        self.set('lines', lines)
        self.set('asymptotes', [])


class DefaultFunction(Function):

    def __init__(self, name='undefined', config_data=None):
        function = eval(config_data['formula'])
        X = eval(config_data['linspace'])
        derivatives = [eval(derivative) for derivative in config_data.get('derivatives', [])]
        super().__init__(function, [X], name, user_derivatives=derivatives, asymptotes=None)
        self.set('lines', [Line2D(X, function(X))])
        self.set('aspect', 'equal' if config['plot_parameters']['aspect'] == 'equal' else 'auto')
        if 'xticks_data' in config_data:
            self.set('xticks', eval(config_data['xticks_data']['xticks']))
            self.set('xticklabels', eval(config_data['xticks_data']['xticklabels']))
