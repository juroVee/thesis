import warnings
from collections import defaultdict

import numpy as np
from matplotlib.lines import Line2D
from scipy.misc import derivative
from scipy.optimize import newton

from .util import signchanges, prepare
from ...config import config


class ComputationsHandler:

    def __init__(self, function):
        self.function = function
        self.f = function.get('f')
        self.x_values = function.get('x_values')
        self.original_x_values = function.get('original_x_values')
        self.user_primes = function.get('user_derivatives')
        self.primes = function.get('derivatives')
        self.maxiter = function.get('zero_points_iterations')
        self.round = self.function.get('rounding')

    def main_function(self) -> None:
        Y_values = [self.f(Xi) for Xi in self.x_values]
        lines = [Line2D(Xi, Yi) for Xi, Yi in zip(self.x_values, Y_values)]
        self.function.set('lines', lines)

    def derivatives(self) -> list:
        derivatives = defaultdict(dict)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                for n in range(1, config['derivative']['user_max'] + 1):
                    if n in self.user_primes:
                        d = self.user_primes[n]
                        derivatives[f'X{i}'][n] = d(X)
                    else:
                        order = n + 1 if n % 2 == 0 else n + 2
                        derivatives[f'X{i}'][n] = derivative(self.f, X, dx=0.001, n=n, order=order)
        self.function.set('derivatives', derivatives)
        self.primes = derivatives
        return w

    def zero_points(self) -> list:
        fprime, fprime2 = self.user_primes.get(1, None), self.user_primes.get(2, None)
        result = []
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, (original_X, X) in enumerate(zip(self.original_x_values, self.x_values)):
                delta_x = np.diff(X)[0]
                candidates = newton(self.f, original_X, fprime=fprime, fprime2=fprime2, tol=delta_x,
                                          maxiter=self.maxiter)
                candidates = candidates[(candidates >= np.amin(X)) & (candidates <= np.amax(X))]
                candidates = candidates[np.isclose(self.f(candidates), 0, atol=10**(-self.round))]
                result.append(candidates)
        self.function.set('zero_points', prepare(result, self.round, concat=True))
        return w

    def extremes(self) -> list:
        result = defaultdict(list)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                table = np.dstack((X, self.primes[f'X{i}'][1], self.primes[f'X{i}'][2]))[0]
                for i0, i1 in signchanges(table[:, 1]):
                    candidates = np.vstack([table[i0], table[i1]])
                    extrema, fprime1, fprime2 = candidates[(np.abs(candidates[:, 1])).argmin()]
                    if fprime2 > 0:
                        result['minima'].append(extrema)
                    elif fprime2 < 0:
                        result['maxima'].append(extrema)
        self.function.set('local_minima', prepare(result['minima'], self.round))
        self.function.set('local_maxima', prepare(result['maxima'], self.round))
        self.function.set('local_extrema', prepare([result['minima'], result['maxima']], self.round, concat=True))
        return w

    def inflex_points(self) -> list:
        result = []
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                table = np.dstack((X, self.primes[f'X{i}'][2], self.primes[f'X{i}'][3]))[0]
                for i0, i1 in signchanges(table[:, 1]):
                    candidates = np.vstack([table[i0], table[i1]])
                    inflex_point, fprime2, fprime3 = candidates[(np.abs(candidates[:, 1])).argmin()]
                    if fprime3 != 0:
                        result.append(inflex_point)
        self.function.set('inflex_points', prepare(result, self.round))
        return w

    def monotonic(self) -> list:
        inc, dec = defaultdict(list), defaultdict(list)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                stacked = np.dstack((X, self.primes[f'X{i}'][1]))[0]
                for interval in np.split(stacked, np.where(np.diff(stacked[:, 1] < 0))[0] + 1):
                    X, fprime1 = np.around(interval[:, 0], self.round), interval[:, 1]
                    if np.all(fprime1 >= 0):
                        inc['values'].append(X)
                        inc['intervals'].append((X[0], X[-1]))
                    else:
                        dec['values'].append(X)
                        dec['intervals'].append((X[0], X[-1]))
        self.function.set('increasing_values', inc['values'])
        self.function.set('increasing_intervals', inc['intervals'])
        self.function.set('decreasing_values', dec['values'])
        self.function.set('decreasing_intervals', dec['intervals'])
        return w

    def concave(self) -> list:
        concave_down, concave_up = defaultdict(list), defaultdict(list)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                stacked = np.dstack((X, self.primes[f'X{i}'][2]))[0]
                for interval in np.split(stacked, np.where(np.diff(stacked[:, 1] < 0))[0] + 1):
                    X, fprime2 = np.around(interval[:, 0], self.round), interval[:, 1]
                    if np.all(fprime2 >= 0):
                        concave_up['values'].append(X)
                        concave_up['intervals'].append((X[0], X[-1]))
                    else:
                        concave_down['values'].append(X)
                        concave_down['intervals'].append((X[0], X[-1]))
        self.function.set('concave_up_values', concave_up['values'])
        self.function.set('concave_up_intervals', concave_up['intervals'])
        self.function.set('concave_down_values', concave_down['values'])
        self.function.set('concave_down_intervals', concave_down['intervals'])
        return w
