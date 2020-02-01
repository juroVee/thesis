# external modules
from scipy.misc import derivative
from scipy.optimize import newton
import numpy as np
from matplotlib.lines import Line2D
import warnings

# project-level modules
from ..config import config


def calculate_main_function(function) -> None:
    f = function.get_parameter('f')
    X_values = function.get_parameter('x_values')
    Y_values = [f(Xi) for Xi in X_values]
    lines = [Line2D(Xi, Yi) for Xi, Yi in zip(X_values, Y_values)]
    function.set_parameter('y_values', Y_values)
    function.set_parameter('lines', lines)


def calculate_zero_points(function, method='newton'):
    # necessary data
    f = function.get_parameter('f')
    X_values = function.get_parameter('x_values')
    derivatives = function.get_parameter('user_derivatives')
    fprime = derivatives[0] if len(derivatives) > 0 else None

    # Newton method
    if method == 'newton':

        # prepare result list
        result = []

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            for X in X_values:

                # get candidates

                candidates = newton(f, X, fprime=fprime, tol=10**(-10), maxiter=50)

                # filter candidates outside interval
                candidates = candidates[(candidates >= np.amin(X)) & (candidates <= np.amax(X))]

                # filter unique values
                candidates = np.unique(candidates)

                # filter values x, where f(x) is really close to zero (test)
                candidates = candidates[np.isclose(f(candidates), 0)]

                for candidate in candidates:
                    result.append(candidate)


            # save values to Function object
            function.set_parameter('zero_points_values', result)
            return True, w


def calculate_derivatives(function) -> None:
    def _derive(X, n):
        order = n + 1 if n % 2 == 0 else n + 2
        return derivative(f, X, dx=0.001, n=n, order=order)
    f = function.get_parameter('f')
    X_values, Y_values = function.get_parameter('x_values'), function.get_parameter('y_values')
    derivatives = {}
    for X, Y in zip(X_values, Y_values):
        for n in range(1, config['derivative']['max_derivative'] + 1):
            if len(function.get_parameter('user_derivatives')) >= n:
                d = function.get_parameter('user_derivatives')[n - 1]
                derivatives[n] = (X, d(X))
            else:
                dydx = _derive(X, n)
                derivatives[n] = (X, dydx)
    function.set_parameter('derivatives', derivatives)


class Calculator:
    pass


calculator = Calculator()