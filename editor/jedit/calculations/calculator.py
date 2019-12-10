# external modules
from scipy.misc import derivative
from scipy.optimize import newton, brentq, bisect
import numpy as np

# package-level modules

# project-level modules


class Calculator:

    def __init__(self, f):
        self.f = f

    def derive(self, X, n):
        order = n + 1 if n % 2 == 0 else n + 2
        return X, derivative(self.f, X, dx=0.001, n=n, order=order)

    def _find_sign_change(self, X):
        return np.where(np.diff(np.signbit(self.f(X))))[0]

    def zero_points(self, X, method='newton'):
        indexes = self._find_sign_change(X)
        sign_changes = zip(indexes, np.add(1, indexes))
        for i, j in sign_changes:
            if method == 'newton':
                yield newton(self.f, X[i])
            elif method == 'brentq':
                yield brentq(self.f, X[i], X[j])
            elif method == 'bisect':
                yield bisect(self.f, X[i], X[j])