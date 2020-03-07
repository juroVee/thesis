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
        result = []
        not_converged_list = []
        zero_derivatives_occured_list = []
    
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
    
            # for each interval Xi (if not continuous)
            for original_X, X in zip(original_X_values, X_values):
    
                # get delta_x (tolerance)
                delta_x = np.diff(X)[0]
    
                # get candidates
                try:
                    candidates, converged, zero_der = newton(f, original_X, fprime=fprime, tol=delta_x, maxiter=maxiter, full_output=True)
                except RuntimeError as e:
                    return True, (w, [], [])
    
                # save info about points where method didn't converge or zero derivation occured
                not_converged = candidates[converged == False]
                zero_der_occured = candidates[zero_der]
    
                # filter candidates outside interval
                candidates = candidates[(candidates >= np.amin(X)) & (candidates <= np.amax(X))]
    
                # get rid of really small numbers that are basically similar
                candidates = np.unique(np.around(candidates, r))
    
                # filter values x, where f(x) is really close to zero (test)
                candidates = candidates[np.isclose(f(candidates), 0)]
    
                for candidate in candidates:
                    result.append(candidate)
    
                for not_conv in not_converged:
                    not_converged_list.append(not_conv)
    
                for zero_d in zero_der_occured:
                    zero_derivatives_occured_list.append(zero_d)
    
    
            # save values to Function object
            self.function.set_parameter('zero_points_values', result)
            return True, (w, not_converged_list, zero_derivatives_occured_list)
    
    def extremes(self) -> tuple:
        # necessary data
        f = self.function.get_parameter('f')
        X_values = self.function.get_parameter('x_values')
    
        # prepare result list
        local_minima, local_maxima = [], []
    
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
    
            for X in X_values:
                fX = f(X)
                minimaX, maximaX = X[argrelextrema(fX, np.less)], X[argrelextrema(fX, np.greater)]
                local_minima.append(minimaX)
                local_maxima.append(maximaX)
    
        local_minima, local_maxima = np.asarray(local_minima).flatten(), np.asarray(local_maxima).flatten()
        self.function.set_parameter('local_minima_xvals', local_minima if len(local_minima) > 0 else [])
        self.function.set_parameter('local_maxima_xvals', local_maxima if len(local_maxima) > 0 else [])
        self.function.set_parameter('local_minima_yvals', f(local_minima) if len(local_minima) > 0 else [])
        self.function.set_parameter('local_maxima_yvals', f(local_maxima) if len(local_maxima) > 0 else [])
        return True, (w, [], [])
    
    def inflex_points(self) -> None:
        # necessary data
        f = self.function.get_parameter('f')
        derivatives = self.function.get_parameter('derivatives')
    
        # prepare result list
        result = []
        for primes in derivatives.values():
            X, fprime = primes[1]
            minimaX, maximaX = X[argrelextrema(fprime, np.less)], X[argrelextrema(fprime, np.greater)]
            for minx in minimaX:
                result.append(minx)
            for maxx in maximaX:
                result.append(maxx)
    
        result = np.asarray(result)
        self.function.set_parameter('inflex_points_xvals', result)
        self.function.set_parameter('inflex_points_yvals', f(result))
    
    def monotonic(self):
        f = self.function.get_parameter('f')
        X_values = self.function.get_parameter('x_values')
    
        result1, result2 = [], []
        result1_intervals, result2_intervals = [], []
    
        local_minima_xvals = self.function.get_parameter('local_minima_xvals')
        local_maxima_xvals = self.function.get_parameter('local_maxima_xvals')
        for X in X_values:
            start, end = X[:1], X[-1:]
            full = np.sort(np.concatenate([start, local_minima_xvals, local_maxima_xvals, end]))
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
    
        self.function.set_parameter(f'increasing_xvals', result2)
        self.function.set_parameter(f'increasing_intervals', result2_intervals)
        self.function.set_parameter(f'decreasing_xvals', result1)
        self.function.set_parameter(f'decreasing_intervals', result1_intervals)
    
    def convex(self):
        X_values = self.function.get_parameter('x_values')
        inflex_points = self.function.get_parameter('inflex_points_xvals')
        fprimes = self.function.get_parameter('derivatives')
    
        result1, result2 = [], []
        result1_intervals, result2_intervals = [], []
        for i in range(len(X_values)):
            X, fprime2 = fprimes[f'X{i}'][2]
            start, end = X[:1], X[-1:]
            full = np.sort(np.concatenate([start, inflex_points, end]))
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
    
        self.function.set_parameter(f'convex_xvals', result1)
        self.function.set_parameter(f'convex_intervals', result1_intervals)
        self.function.set_parameter(f'concave_xvals', result2)
        self.function.set_parameter(f'concave_intervals', result2_intervals)
    
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