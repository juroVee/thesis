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
        self.refinement = function.get('refinement')
        self.maxiter = function.get('zero_points_iterations')
        self.round = self.function.get('rounding')
        self.data = function.get_analysis_data()

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
        for i, X in enumerate(self.x_values):
            key = f'X{i}'
            for n in range(1, settings['derivative']['user_max'] + 1):
                if n in self.user_primes:
                    d = self.user_primes[n]
                    values = d(X)
                else:
                    values = get_derivative(self.f, X, n)
                self.data[f'primes{n}'][key] = values

    def zero_points(self) -> None:
        fprime, fprime2 = self.user_primes.get(1, None), self.user_primes.get(2, None)
        np.set_printoptions(suppress=True)
        for i, (original_X, X) in enumerate(zip(self.original_x_values, self.x_values)):
            key = f'X{i}'
            delta_x = np.diff(X)[0]
            candidates = newton(self.f, original_X, fprime=fprime, fprime2=fprime2, tol=delta_x,
                                      maxiter=self.maxiter)
            candidates = candidates[(candidates >= np.amin(X)) & (candidates <= np.amax(X))]
            candidates = candidates[np.isclose(self.f(candidates), 0, atol=10**(-self.round))]
            self.data['zero_points'][key] = prepare(candidates, self.round)

    def extremes(self) -> None:
        for i, X in enumerate(self.x_values):
            key = f'X{i}'
            primes1 = approximate_zeros(self.data['primes1'][key])
            for n in range(2, settings['extremes']['max_derivative'] + 1, 2): # kazda parna podla Vety 17
                next_prime = self.data[f'primes{n}'].get(key)
                if next_prime is None:
                    next_prime = get_derivative(self.f, X, n)
                next_prime = approximate_zeros(next_prime)
                table = np.dstack((X, primes1, next_prime))[0]
                candidates = table[table[:, 1] == 0]
                if len(candidates) == 0:
                    break
                if np.any(candidates[candidates[:, 2] != 0]) and n % 2 == 0:
                    minima, maxima = candidates[candidates[:, 2] > 0][:, 0], candidates[candidates[:, 2] < 0][:, 0]
                    self.data['minima'][key] = prepare(minima, self.round)
                    self.data['maxima'][key] = prepare(maxima, self.round)
                    self.data['extremes'][key] = prepare(np.concatenate([minima, maxima]), self.round)
                    if not np.any(candidates[candidates[:, 2] == 0]):
                        break

    def inflex_points(self) -> None:
        for i, X in enumerate(self.x_values):
            key = f'X{i}'
            fprime2 = approximate_zeros(self.data['primes2'][key])
            fprime3 = approximate_zeros(self.data['primes3'][key])
            table = np.dstack((X, fprime2, fprime3))[0]
            candidates = table[table[:, 1] == 0]
            self.data['inflex_points'][key] = prepare(candidates[candidates[:, 2] != 0][:, 0], self.round)

    def monotonic(self) -> None:
        for i, X in enumerate(self.x_values):
            key, increasing, decreasing = f'X{i}', [], []
            fprime1 = approximate_zeros(self.data['primes1'][key])
            table = np.dstack((X, fprime1))[0]
            table = np.delete(table, np.where(table[:, 1] == 0)[0], axis=0)
            intervals = np.split(table, np.where(np.diff(table[:, 1] < 0))[0] + 1)
            for interval in intervals:
                if len(interval) > 1:
                    X, fprime1 = interval[:, 0], interval[:, 1]
                    dest = increasing if np.all(fprime1 > 0) else decreasing
                    dest.append(prepare(X, self.round))
            self.data['increasing'][key] = increasing
            self.data['decreasing'][key] = decreasing

    def concave(self) -> None:
        for i, X in enumerate(self.x_values):
            key, concave_down, concave_up = f'X{i}', [], []
            fprime2 = approximate_zeros(self.data['primes2'][key])
            table = np.dstack((X, fprime2))[0]
            table = np.delete(table, np.where(table[:, 1] == 0)[0], axis=0)
            intervals = np.split(table, np.where(np.diff(table[:, 1] < 0))[0] + 1)
            for interval in intervals:
                if len(interval) > 1:
                    X, fprime2 = np.around(interval[:, 0], self.round), interval[:, 1]
                    dest = concave_up if np.all(fprime2 > 0) else concave_down
                    dest.append(prepare(X, self.round))
            self.data['concave_down'][key] = concave_down
            self.data['concave_up'][key] = concave_up
