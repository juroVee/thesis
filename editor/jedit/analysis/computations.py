from collections import defaultdict

import numpy as np
from matplotlib.lines import Line2D
from scipy.optimize import newton

from .util import prepare, approximate_zeros, get_derivative
from ..settings import settings


class ComputationsManager:

    def __init__(self, function):
        self.function = function
        self.f = function.get('f')
        self.x_values = function.get('x_values')
        self.original_x_values = function.get('original_x_values')
        self.user_primes = function.get('user_derivatives')
        self.primes = function.get('derivatives')
        self.refinement = function.get('refinement')
        self.maxiter = function.get('zero_points_iterations')
        self.round = self.function.get('rounding')

    def main_function(self) -> None:
        if self.refinement == 1:
            self.function.set('x_values', self.original_x_values)
            self.x_values = self.original_x_values
        else:
            new_x_values = []
            for X in self.original_x_values:
                minima, maxima, intervals = min(X), max(X), len(X) - 1
                new_intervals = intervals * self.refinement
                new_X = np.linspace(minima, maxima, new_intervals + 1)
                with np.errstate(divide='ignore', invalid='ignore'):
                    new_x_values.append(new_X[~np.isnan(self.f(new_X))])
            self.function.set('x_values', new_x_values)
            self.x_values = new_x_values
        y_values = [self.f(Xi) for Xi in self.x_values]
        lines = [Line2D(Xi, Yi) for Xi, Yi in zip(self.x_values, y_values)]
        self.function.set('lines', lines)

    def main_derivatives(self) -> None:
        result = defaultdict(dict)
        for i, X in enumerate(self.x_values):
            for n in range(1, settings['derivative']['user_max'] + 1):
                if n in self.user_primes:
                    d = self.user_primes[n]
                    values = d(X)
                else:
                    values = get_derivative(self.f, X, n)
                result[f'X{i}'][n] = values
        self.function.set('derivatives', result)
        self.primes = result

    def zero_points(self) -> None:
        fprime, fprime2 = self.user_primes.get(1, None), self.user_primes.get(2, None)
        result = set()
        for i, (original_X, X) in enumerate(zip(self.original_x_values, self.x_values)):
            delta_x = np.diff(X)[0]
            candidates = newton(self.f, original_X, fprime=fprime, fprime2=fprime2, tol=delta_x,
                                      maxiter=self.maxiter)
            candidates = candidates[(candidates >= np.amin(X)) & (candidates <= np.amax(X))]
            candidates = candidates[np.isclose(self.f(candidates), 0, atol=10**(-self.round))]
            result.update(candidates)
        self.function.set('zero_points', prepare(result, self.round))

    def extremes(self) -> None:
        result = defaultdict(set)
        np.set_printoptions(suppress=True)
        for i, X in enumerate(self.x_values):
            primes1 = approximate_zeros(self.primes[f'X{i}'][1])
            for n in range(2, settings['extremes']['max_derivative'] + 1, 2):
                next_prime = self.primes[f'X{i}'].get(n)
                if next_prime is None:
                    next_prime = get_derivative(self.f, X, n)
                next_prime = approximate_zeros(next_prime)
                table = np.dstack((X, primes1, next_prime))[0]
                candidates = table[table[:, 1] == 0]
                if len(candidates) == 0:
                    break
                if np.any(candidates[candidates[:, 2] != 0]) and n % 2 == 0:
                    result['minima'].update(candidates[candidates[:, 2] > 0][:, 0])
                    result['maxima'].update(candidates[candidates[:, 2] < 0][:, 0])
                    if not np.any(candidates[candidates[:, 2] == 0]):
                        break
        self.function.set('local_minima', prepare(result['minima'], self.round))
        self.function.set('local_maxima', prepare(result['maxima'], self.round))
        self.function.set('local_extrema', prepare(result['minima'] | result['maxima'], self.round))

    def inflex_points(self) -> None:
        result = set()
        for i, X in enumerate(self.x_values):
            fprime2 = approximate_zeros(self.primes[f'X{i}'][2])
            fprime3 = approximate_zeros(self.primes[f'X{i}'][3])
            table = np.dstack((X, fprime2, fprime3))[0]
            candidates = table[table[:, 1] == 0]
            result.update(candidates[candidates[:, 2] != 0][:, 0])
        self.function.set('inflex_points', prepare(result, self.round))

    def monotonic(self) -> None:
        increasing, decreasing = defaultdict(list), defaultdict(list)
        for i, X in enumerate(self.x_values):
            fprime1 = approximate_zeros(self.primes[f'X{i}'][1])
            table = np.dstack((X, fprime1))[0]
            table = np.delete(table, np.where(table[:, 1] == 0)[0], axis=0)
            intervals = np.split(table, np.where(np.diff(table[:, 1] < 0))[0] + 1)
            for interval in intervals:
                X, fprime1 = interval[:, 0], interval[:, 1]
                dest = increasing if np.all(fprime1 > 0) else decreasing
                dest['values'].append(X)
                dest['intervals'].append((X[0], X[-1]))
        self.function.set('increasing_values', increasing['values'])
        self.function.set('increasing_intervals', increasing['intervals'])
        self.function.set('decreasing_values', decreasing['values'])
        self.function.set('decreasing_intervals', decreasing['intervals'])

    def concave(self) -> None:
        concave_down, concave_up = defaultdict(list), defaultdict(list)
        for i, X in enumerate(self.x_values):
            fprime2 = approximate_zeros(self.primes[f'X{i}'][2])
            table = np.dstack((X, fprime2))[0]
            table = np.delete(table, np.where(table[:, 1] == 0)[0], axis=0)
            intervals = np.split(table, np.where(np.diff(table[:, 1] < 0))[0] + 1)
            for interval in intervals:
                X, fprime2 = np.around(interval[:, 0], self.round), interval[:, 1]
                dest = concave_up if np.all(fprime2 >= 0) else concave_down
                dest['values'].append(X)
                dest['intervals'].append((X[0], X[-1]))
        self.function.set('concave_up_values', concave_up['values'])
        self.function.set('concave_up_intervals', concave_up['intervals'])
        self.function.set('concave_down_values', concave_down['values'])
        self.function.set('concave_down_intervals', concave_down['intervals'])
