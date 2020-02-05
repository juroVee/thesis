# external modules
from scipy.misc import derivative
from scipy.optimize import newton
import numpy as np
from matplotlib.lines import Line2D
import warnings
from collections import defaultdict

# project-level modules
from ..config import config


def calculate_main_function(function) -> None:
    # necessary data
    f = function.get_parameter('f')
    X_values = function.get_parameter('x_values')

    # calculate fvals (Y_values)
    Y_values = [f(Xi) for Xi in X_values]

    # prepare lines for plotting
    lines = [Line2D(Xi, Yi) for Xi, Yi in zip(X_values, Y_values)]

    # save values to Function object
    function.set_parameter('y_values', Y_values)
    function.set_parameter('lines', lines)


def calculate_zero_points(function, method='newton'):
    # necessary data
    f = function.get_parameter('f')
    original_X_values = function.get_parameter('original_x_values')
    X_values = function.get_parameter('x_values')
    derivatives = function.get_parameter('user_derivatives')
    fprime = derivatives[0] if len(derivatives) > 0 else None
    maxiter = function.get_parameter('zero_points_iterations')
    r = config['zero_points']['round']

    # Newton method
    if method == 'newton':

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
                candidates, converged, zero_der = newton(f, original_X, fprime=fprime, tol=delta_x, maxiter=maxiter, full_output=True)

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
            function.set_parameter('zero_points_values', result)
            return True, (w, not_converged_list, zero_derivatives_occured_list)


def calculate_derivatives(function) -> None:
    # necessary data
    f = function.get_parameter('f')
    X_values= function.get_parameter('x_values')

    # allocate structure for saving derivative values
    derivatives = defaultdict(dict)

    # for each interval Xi (if not continuous)
    for i, X in enumerate(X_values):

        # count nth derivative from scipy.misc.derivative or use user provided derivatives
        for n in range(1, config['derivative']['max_derivative'] + 1):
            if len(function.get_parameter('user_derivatives')) >= n:
                d = function.get_parameter('user_derivatives')[n - 1]
                derivatives[f'X{i}'][n] = (X, d(X))
            else:
                order = n + 1 if n % 2 == 0 else n + 2
                derivatives[f'X{i}'][n] = (X, derivative(f, X, dx=0.001, n=n, order=order))

    # save values to Function object
    function.set_parameter('derivatives', derivatives)