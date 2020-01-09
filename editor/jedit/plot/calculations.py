# external modules
from scipy.misc import derivative
from scipy.optimize import newton, brentq, bisect
import numpy as np


class Calculator:

    def __init__(self, f):
        self.f = f

    def _find_sign_changes(self, X):
        return np.where(np.diff(np.signbit(np.around(self.f(X), 8))))[0]

    def derive(self, X, n):
        order = n + 1 if n % 2 == 0 else n + 2
        return X, derivative(self.f, X, dx=0.001, n=n, order=order)

    def zero_points(self, X, method='newton'):
        indexes = self._find_sign_changes(X)
        sign_changes = zip(indexes, np.add(1, indexes))

        try:
            if method == 'newton':
                return [newton(self.f, X[i]) for i, j in sign_changes]
            elif method == 'brentq':
                return [brentq(self.f, X[i], X[j]) for i, j in sign_changes]
            elif method == 'bisect':
                return [bisect(self.f, X[i], X[j]) for i, j in sign_changes]
        except RuntimeError:
            return None