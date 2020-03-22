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
from ..util import flatten

class Calculator:
    
    def __init__(self, function):
        self.function = function

    def main_function(self) -> None:
        # necessary data
        f = self.function.get_parameter('f')
        X_values = self.function.get_parameter('x_values')
    
        # calculate fvals (Y_values)
        Y_values = [f(Xi) for Xi in X_values]
    
        # prepare lines for plotting
        lines = [Line2D(Xi, Yi) for Xi, Yi in zip(X_values, Y_values)]
    
        # save values to Function object
        self.function.set_parameter('y_values', Y_values)
        self.function.set_parameter('lines', lines)
    
    def zero_points(self) -> tuple:
        # necessary data
        f = self.function.get_parameter('f')
        original_X_values = self.function.get_parameter('original_x_values')
        X_values = self.function.get_parameter('x_values')
        derivatives = self.function.get_parameter('user_derivatives')
        fprime = derivatives[0] if len(derivatives) > 0 else None
        maxiter = self.function.get_parameter('zero_points_iterations')
        r = config['zero_points']['round']
    
        # prepare result list
        result = defaultdict()
        not_converged_list = []
        zero_derivatives_occured_list = []
    
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
    
            # for each interval Xi (if not continuous)
            for i, (original_X, X) in enumerate(zip(original_X_values, X_values)):
                key = f'X{i}'
    
                # get delta_x (tolerance)
                delta_x = np.diff(X)[0]
    
                # get candidates
                try:
                    candidates, converged, zero_der = newton(f, original_X, fprime=fprime, tol=delta_x, maxiter=maxiter, full_output=True)
                except RuntimeError as e:
                    break
    
                # save info about points where method didn't converge or zero derivation occured
                not_converged = candidates[converged == False]
                zero_der_occured = candidates[zero_der]
    
                # filter candidates outside interval
                candidates = candidates[(candidates >= np.amin(X)) & (candidates <= np.amax(X))]
    
                # get rid of really small numbers that are basically similar
                candidates = np.unique(np.around(candidates, r))
    
                # filter values x, where f(x) is really close to zero (test) and save
                result[key] = candidates[np.isclose(f(candidates), 0)]
    
                for not_conv in not_converged:
                    not_converged_list.append(not_conv)
    
                for zero_d in zero_der_occured:
                    zero_derivatives_occured_list.append(zero_d)
    
            # save values to Function object
            self.function.set_parameter('zero_points_dataset', result)
            return True, (w, not_converged_list, zero_derivatives_occured_list)
    
    def extremes(self) -> tuple:
        # necessary data
        f = self.function.get_parameter('f')
        X_values = self.function.get_parameter('x_values')
        # prepare results structure
        result = defaultdict(dict)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            for i, X in enumerate(X_values):
                key = f'X{i}'
                fX = f(X)
                result[key]['minima'] = X[argrelextrema(fX, np.less)]
                result[key]['maxima'] = X[argrelextrema(fX, np.greater)]
        self.function.set_parameter('extremes_dataset', result)
        return True, (w, [], [])
    
    def inflex_points(self) -> None:
        # necessary data
        X_values = self.function.get_parameter('x_values')
        primes = self.function.get_parameter('derivatives')
        # prepare result list
        result = defaultdict()
        for i, X in enumerate(X_values):
            key = f'X{i}'
            _, fprime = primes[key][1]
            result[key] = np.concatenate([X[argrelextrema(fprime, np.less)], X[argrelextrema(fprime, np.greater)]])
        self.function.set_parameter('inflex_points_dataset', result)
    
    def monotonic(self):
        f = self.function.get_parameter('f')
        X_values = self.function.get_parameter('x_values')
        dataset = self.function.get_parameter('extremes_dataset')
        result_inc, result_dec = defaultdict(dict), defaultdict(dict)

        for i, X in enumerate(X_values):
            key = f'X{i}'
            start, end = X[:1], X[-1:]
            local_minima_xvals = dataset[key]['minima']
            local_maxima_xvals = dataset[key]['maxima']
            full = np.sort(np.concatenate([start, local_minima_xvals, local_maxima_xvals, end]))
            result1, result2 = [], []
            result1_intervals, result2_intervals = [], []
            if len(full) > 2:
                pairs = [(full[i], full[i + 1]) for i in range(len(full) - 1)]
                for j, (x1, x2) in enumerate(pairs):
                    if j == 0:
                        interval = X[(X >= x1) & (X < x2)]
                    elif j == len(pairs) - 1:
                        interval = X[(X > x1) & (X <= x2)]
                    else:
                        interval = X[(X > x1) & (X < x2)]
                    if f(x1) > f(x2):
                        result1.append(interval)
                        result1_intervals.append((x1, x2))
                    else:
                        result2.append(interval)
                        result2_intervals.append((x1, x2))
            elif len(full) == 2:
                x1, x2 = full
                interval = X[(X >= x1) & (X <= x2)]
                if f(x1) > f(x2):
                    result1.append(interval)
                    result1_intervals.append((x1, x2))
                else:
                    result2.append(interval)
                    result2_intervals.append((x1, x2))

            result_inc[key]['values'] = result2
            result_dec[key]['values'] = result1
            result_inc[key]['intervals'] = result2_intervals
            result_dec[key]['intervals'] = result1_intervals

        self.function.set_parameter('increasing_dataset', result_inc)
        self.function.set_parameter('decreasing_dataset', result_dec)
    
    def convex(self):
        X_values = self.function.get_parameter('x_values')
        inflex_points = flatten(self.function.get_parameter('inflex_points_dataset'))
        primes = self.function.get_parameter('derivatives')
        result_convex, result_concave = defaultdict(dict), defaultdict(dict)

        for i, X in enumerate(X_values):
            key = f'X{i}'
            _, fprime2 = primes[key][2]
            start, end = X[:1], X[-1:]
            full = np.sort(np.concatenate([start, inflex_points, end]))
            result1, result2 = [], []
            result1_intervals, result2_intervals = [], []
            if len(full) > 2:
                pairs = [(full[i], full[i + 1]) for i in range(len(full) - 1)]
                for j, (x1, x2) in enumerate(pairs):
                    if j == 0:
                        cond = (X >= x1) & (X < x2)
                    elif j == len(pairs) - 1:
                        cond = (X > x1) & (X <= x2)
                    else:
                        cond = (X > x1) & (X < x2)
                    interval = X[cond]
                    fprime2_interval = fprime2[cond]
                    if fprime2_interval[len(fprime2_interval) // 2] > 0:
                        result1.append(interval)
                        result1_intervals.append((x1, x2))
                    else:
                        result2.append(interval)
                        result2_intervals.append((x1, x2))
                result_convex[key]['values'] = result1
                result_concave[key]['values'] = result2
                result_convex[key]['intervals'] = result1_intervals
                result_concave[key]['intervals'] = result2_intervals

            self.function.set_parameter('convex_dataset', result_convex)
            self.function.set_parameter('concave_dataset', result_concave)
    
    def derivatives(self) -> None:
        # necessary data
        f = self.function.get_parameter('f')
        X_values= self.function.get_parameter('x_values')
    
        # allocate structure for saving derivative values
        derivatives = defaultdict(dict)
    
        # for each interval Xi (if not continuous)
        for i, X in enumerate(X_values):
    
            # count nth derivative from scipy.misc.derivative or use user provided derivatives
            for n in range(1, config['derivative']['max_derivative'] + 1):
                if len(self.function.get_parameter('user_derivatives')) >= n:
                    d = self.function.get_parameter('user_derivatives')[n - 1]
                    derivatives[f'X{i}'][n] = (X, d(X))
                else:
                    order = n + 1 if n % 2 == 0 else n + 2
                    derivatives[f'X{i}'][n] = (X, derivative(f, X, dx=0.001, n=n, order=order))
    
        # save values to Function object
        self.function.set_parameter('derivatives', derivatives)