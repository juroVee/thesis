from collections import defaultdict

import numpy as np
import warnings
from matplotlib.lines import Line2D
from scipy.misc import derivative
from scipy.optimize import newton

from ...config import config
from .util import signchanges, around


class ComputationsHandler:

    def __init__(self, function):
        self.function = function
        self.f = function.get('f')
        self.x_values = function.get('x_values')
        self.original_x_values = function.get('original_x_values')
        self.user_primes = function.get('user_derivatives')
        self.primes = function.get('derivatives')
        self.maxiter = function.get('zero_points_iterations')
        self.refinement_y = function.get('refinement_y')
        self.round = config['editor_settings']['default_round']

    def main_function(self) -> None:
        Y_values = [self.f(Xi) for Xi in self.x_values]
        lines = [Line2D(Xi, Yi) for Xi, Yi in zip(self.x_values, Y_values)]
        self.function.set('y_values', Y_values)
        self.function.set('lines', lines)

    def derivatives(self) -> None:
        derivatives = defaultdict(dict)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                key = f'X{i}'
                for n in range(1, config['derivative']['user_max'] + 1):
                    if n in self.user_primes:
                        d = self.user_primes[n]
                        derivatives[key][n] = d(X)
                    else:
                        order = n + 1 if n % 2 == 0 else n + 2
                        derivatives[key][n] = derivative(self.f, X, dx=0.001, n=n, order=order)
        self.function.set('derivatives', derivatives)
        self.primes = derivatives
        return w

    def zero_points(self) -> tuple:
        fprime, fprime2 = self.user_primes.get(1, None), self.user_primes.get(2, None)
        result = defaultdict()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, (original_X, X) in enumerate(zip(self.original_x_values, self.x_values)):
                key = f'X{i}'
                delta_x = np.diff(X)[0]
                ref = abs(self.refinement_y)
                delta_y = delta_x * ref if self.refinement_y >= 0 else delta_x / ref
                try:
                    candidates = newton(self.f, original_X, fprime=fprime, fprime2=fprime2, tol=delta_x, maxiter=self.maxiter)
                except RuntimeError:
                    break
                candidates = candidates[(candidates >= np.amin(X)) & (candidates <= np.amax(X))]
                candidates = np.unique(around(candidates, self.round))
                result[key] = candidates[np.isclose(self.f(candidates), 0, atol=delta_y)]
        self.function.set('zero_points_dataset', result)
        return w

    def extremes(self) -> warnings.WarningMessage:
        result = defaultdict(list)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                key = f'X{i}'
                table = np.dstack((X, self.primes[key][1], self.primes[key][2]))[0]
                for i0, i1 in signchanges(table[:, 1]):
                    candidates = np.vstack([table[i0], table[i1]])
                    extrema, fprime1, fprime2 = candidates[(np.abs(candidates[:, 1])).argmin()]
                    if fprime2 > 0:
                        result['minima'].append(extrema)
                    elif fprime2 < 0:
                        result['maxima'].append(extrema)
        self.function.set('local_minima', np.unique(around(np.asarray(result['minima']), self.round)))
        self.function.set('local_maxima', np.unique(around(np.asarray(result['maxima']), self.round)))
        self.function.set('local_extrema', np.sort(np.unique(around(np.concatenate([result['minima'], result['maxima']]), self.round))))
        return w

    def inflex_points(self) -> warnings.WarningMessage:
        result = list()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                key = f'X{i}'
                table = np.dstack((X, self.primes[key][2], self.primes[key][3]))[0]
                for i0, i1 in signchanges(table[:, 1]):
                    candidates = np.vstack([table[i0], table[i1]])
                    inflex_point, fprime2, fprime3 = candidates[(np.abs(candidates[:, 1])).argmin()]
                    if fprime3 != 0:
                        result.append(inflex_point)
        self.function.set('inflex_points', np.unique(around(np.asarray(result), self.round)))
        return w

    def monotonic(self):
        result_inc, result_dec = defaultdict(list), defaultdict(list)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                key = f'X{i}'
                stacked = np.dstack((X, self.primes[key][1]))[0]
                for interval in np.split(stacked, np.where(np.diff(stacked[:, 1] < 0))[0] + 1):
                    X, primes = around(interval[:, 0], self.round), interval[:, 1]
                    dest = result_inc if np.all(primes >= 0) else result_dec
                    dest['values'].append(X)
                    dest['intervals'].append((X[0], X[-1]))
        self.function.set('increasing_values', result_inc['values'])
        self.function.set('increasing_intervals', result_inc['intervals'])
        self.function.set('decreasing_values', result_dec['values'])
        self.function.set('decreasing_intervals', result_inc['intervals'])
        return w

    def concave(self):
        concave_down, concave_up = defaultdict(list), defaultdict(list)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                key = f'X{i}'
                stacked = np.dstack((X, self.primes[key][2]))[0]
                for interval in np.split(stacked, np.where(np.diff(stacked[:, 1] < 0))[0] + 1):
                    X, primes = around(interval[:, 0], self.round), interval[:, 1]
                    dest = concave_up if np.all(primes >= 0) else concave_down
                    dest['values'].append(X)
                    dest['intervals'].append((X[0], X[-1]))
        self.function.set('concave_up_values', concave_up['values'])
        self.function.set('concave_up_intervals', concave_up['intervals'])
        self.function.set('concave_down_values', concave_down['values'])
        self.function.set('concave_down_intervals', concave_down['intervals'])
        return w
