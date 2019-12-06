# package-level modules

# project-level modules

# external modules
from scipy.misc import derivative
from scipy.optimize import fsolve


class Calculator:

    def __init__(self, f):
        self.f = f

    def derive(self, X, n):
        order = n + 1 if n % 2 == 0 else n + 2
        return X, derivative(self.f, X, dx=0.001, n=n, order=order)

    def zero_points(self):
        """
        Just temporary solution
        :return:
        """
        # zero_points = []
        # for line in self.function.parameters['lines']:
        #     for x, y in zip(line.get_xdata(), line.get_ydata()):
        #         if y == 0:
        #             zero_points.append((x, y))
        # return zero_points
        return []