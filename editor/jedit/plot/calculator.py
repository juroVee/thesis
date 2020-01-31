# external modules
from scipy.misc import derivative
from scipy import optimize
import numpy as np
from matplotlib.lines import Line2D

# project-level modules
from ..config import config

class Calculator:

    def __init__(self, function):
        self.function = function

    def calculate_main_function(self) -> None:
        f = self.function.get_parameter('f')
        X_values = self.function.get_parameter('x_values')
        Y_values = [f(Xi) for Xi in X_values]
        lines = [Line2D(Xi, Yi) for Xi, Yi in zip(X_values, Y_values)]
        self.function.set_parameter('y_values', Y_values)
        self.function.set_parameter('lines', lines)

    def calculate_derivatives(self) -> None:
        def _derive(X, n):
            order = n + 1 if n % 2 == 0 else n + 2
            return derivative(f, X, dx=0.001, n=n, order=order)
        f = self.function.get_parameter('f')
        X_values, Y_values = self.function.get_parameter('x_values'), self.function.get_parameter('y_values')
        derivatives = {}
        for X, Y in zip(X_values, Y_values):
            for n in range(1, config['derivative']['max_derivative'] + 1):
                if len(self.function.get_parameter('user_derivatives')) >= n:
                    d = self.function.get_parameter('user_derivatives')[n - 1]
                    derivatives[n] = (X, d(X))
                else:
                    dydx = _derive(X, n)
                    derivatives[n] = (X, dydx)
        self.function.set_parameter('derivatives', derivatives)