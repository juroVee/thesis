# external modules
from scipy.misc import derivative
from scipy.optimize import newton
from scipy.signal import argrelextrema
import numpy as np
from matplotlib.lines import Line2D
import warnings
from collections import defaultdict

# project-level modules
from ..config import config

class Calculator:
    
    def __init__(self, function):
        self.function = function
        self.f = function.get_parameter('f')
        self.x_values = function.get_parameter('x_values')
        self.original_x_values = function.get_parameter('original_x_values')
        self.user_primes = function.get_parameter('user_derivatives')
        self.primes = function.get_parameter('derivatives')
        self.maxiter = function.get_parameter('zero_points_iterations')

    def main_function(self) -> None:
        Y_values = [self.f(Xi) for Xi in self.x_values]
        lines = [Line2D(Xi, Yi) for Xi, Yi in zip(self.x_values, Y_values)]
        self.function.set_parameter('y_values', Y_values)
        self.function.set_parameter('lines', lines)
    
    def zero_points(self) -> tuple:
        fprime = self.user_primes[0] if len(self.user_primes) > 0 else None
        r = config['zero_points']['round']
        result = defaultdict()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                key = f'X{i}'
                delta_x = np.diff(X)[0]
                try:
                    candidates, converged, zero_der = newton(self.f, X, fprime=fprime, tol=delta_x, maxiter=self.maxiter, full_output=True)
                except RuntimeError:
                    break
                candidates = candidates[(candidates >= np.amin(X)) & (candidates <= np.amax(X))]
                candidates = np.unique(np.around(candidates, r))
                result[key] = candidates[np.isclose(self.f(candidates), 0)]
            self.function.set_parameter('zero_points_dataset', result)
            return w
    
    def extremes(self) -> tuple:
        result = defaultdict(dict)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                key = f'X{i}'
                fX = self.f(X)
                result[key]['minima'] = X[argrelextrema(fX, np.less)]
                result[key]['maxima'] = X[argrelextrema(fX, np.greater)]
            self.function.set_parameter('extremes_dataset', result)
            return w
    
    def inflex_points(self) -> None:
        result = defaultdict()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                key = f'X{i}'
                _, fprime = self.primes[key][1]
                result[key] = np.concatenate([X[argrelextrema(fprime, np.less)], X[argrelextrema(fprime, np.greater)]])
            self.function.set_parameter('inflex_points_dataset', result)
            return w
    
    def monotonic(self):
        dataset = self.function.get_parameter('extremes_dataset')
        result_inc, result_dec = defaultdict(lambda: defaultdict(list)), defaultdict(lambda: defaultdict(list))
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                key = f'X{i}'
                full = np.sort(np.concatenate([X[:1], dataset[key]['minima'], dataset[key]['maxima'], X[-1:]]))
                pairs = [(full[i], full[i + 1]) for i in range(len(full) - 1)]
                for j, (x1, x2) in enumerate(pairs):
                    interval = X[(X >= x1) & (X <= x2)]
                    dest = result_dec[key] if self.f(x1) > self.f(x2) else result_inc[key]
                    dest['values'].append(interval)
                    dest['intervals'].append((x1, x2))
            self.function.set_parameter('increasing_dataset', result_inc)
            self.function.set_parameter('decreasing_dataset', result_dec)
            return w
    
    def convex(self):
        dataset = self.function.get_parameter('inflex_points_dataset')
        primes = self.function.get_parameter('derivatives')
        result_convex, result_concave = defaultdict(lambda: defaultdict(list)), defaultdict(lambda: defaultdict(list))
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                key = f'X{i}'
                _, fprime2 = primes[key][2]
                full = np.sort(np.concatenate([X[:1], np.concatenate(list(dataset.values())), X[-1:]]))
                pairs = [(full[i], full[i + 1]) for i in range(len(full) - 1)]
                for j, (x1, x2) in enumerate(pairs):
                    interval = X[(X >= x1) & (X <= x2)]
                    fprime2_interval = fprime2[(X >= x1) & (X <= x2)]
                    mid_value = fprime2_interval[len(fprime2_interval) // 2]
                    dest = result_convex[key] if mid_value > 0 else result_concave[key]
                    dest['values'].append(interval)
                    dest['intervals'].append((x1, x2))
            self.function.set_parameter('convex_dataset', result_convex)
            self.function.set_parameter('concave_dataset', result_concave)
            return w
    
    def derivatives(self) -> None:
        derivatives = defaultdict(dict)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(self.x_values):
                for n in range(1, config['derivative']['max_derivative'] + 1):
                    if len(self.user_primes) >= n:
                        d = self.user_primes[n - 1]
                        derivatives[f'X{i}'][n] = (X, d(X))
                    else:
                        order = n + 1 if n % 2 == 0 else n + 2
                        derivatives[f'X{i}'][n] = (X, derivative(self.f, X, dx=0.001, n=n, order=order))
            self.function.set_parameter('derivatives', derivatives)
            self.primes = derivatives
            return w