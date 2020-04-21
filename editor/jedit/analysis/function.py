import numpy as np
import itertools

from matplotlib.lines import Line2D
from collections import defaultdict

from .plotter import Plotter
from ..settings import settings


class Function:
    """
    Trieda reprezentujúca všetky parametre funkcie
    """

    def __init__(self, f, X, name, user_derivatives, asymptotes):
        self.parameters = {}
        self.analysis_data = defaultdict(dict)
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
        self.set('rounding', settings['editor']['round']['default'])

    def _init_plot_parameters(self):
        self.set('grid', True if settings['plot_parameters']['grid'] == 'yes' else False)
        self.set('main_function_color', settings['main_function']['color'])
        for n in range(1, settings['derivative']['user_max'] + 1):
            self.set('derivative_color' + str(n), settings['derivative']['colors'][n - 1])

    def _init_derivatives(self):
        for n in range(1, settings['derivative']['user_max'] + 1):
            self.set('active_derivative' + str(n), False)

    def _init_zero_points(self):
        self.set('zero_points_visible', False)
        if len(self.get('user_derivatives')) == 1:
            self.set('zero_points_method', 'Newton')
        elif len(self.get('user_derivatives')) == 2:
            self.set('zero_points_method', 'Halley')
        else:
            self.set('zero_points_method', 'Secant')
        self.set('zero_points_color', settings['zero_points']['color'])
        self.set('zero_points_iterations', settings['zero_points']['iterations'])

    def _init_analysis(self, op='extremes'):
        self.set(f'{op}_visible', False)
        self.set(f'{op}_color', settings[op]['color'])

    def _init_refinements(self):
        self.set('refinement', 1)

    def plot(self, ax) -> None:
        """
        Pomocou triedy Plotter vykreslí všetky užívateľom zvolené informácie do grafu
        :param ax: objekt matplotlib Axes
        :return:
        """
        ax.clear()
        Plotter(self, ax).plot_all()

    def set(self, parameter_name, parameter_value) -> None:
        """
        Priradí parametru s menom name hodnotu value
        :return:
        """
        self.parameters[parameter_name] = parameter_value

    def get(self, parameter_name):
        """
        Vráti hodnotu parametra, ktorý ma názov parameter_name
        :return:
        """
        return self.parameters.get(parameter_name, None)

    def get_analysis_data(self, key=None, unpack=False, list_values=False) -> np.array:
        if key is None:
            return self.analysis_data
        if unpack and key in self.analysis_data:
            all_intervals = self.analysis_data.get(key)
            if list_values:
                return np.asarray(list(itertools.chain(*all_intervals.values())))
            return np.concatenate(list(all_intervals.values()))
        return self.analysis_data.get(key, np.asarray([]))

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
                self.set(param, getattr(ax, f'get_{param}')())
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
        super().__init__(function, [X], name, user_derivatives={}, asymptotes=[])
        self.set('lines', [Line2D(X, function(X))])
        self.set('aspect', 'equal' if settings['plot_parameters']['aspect'] == 'equal' else 'auto')
        if 'xticks_data' in config_data:
            self.set('xticks', eval(config_data['xticks_data']['xticks']))
            self.set('xticklabels', eval(config_data['xticks_data']['xticklabels']))
