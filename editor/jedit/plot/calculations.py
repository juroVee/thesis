# external modules
from scipy.misc import derivative
from scipy import optimize
import numpy as np


class Calculator:

    def __init__(self, f):
        self.f = f

    def _find_sign_changes(self, X):
        fX = self.f(X)
        fX[fX == 0.] = 0.
        return np.where(np.diff(np.signbit(fX)))[0]

    def derive(self, X, n):
        order = n + 1 if n % 2 == 0 else n + 2
        return X, derivative(self.f, X, dx=0.001, n=n, order=order)

    def zero_points(self, X, method='newton', refinement=1):
        indexes = self._find_sign_changes(X)
        sign_changes = zip(indexes, np.add(1, indexes))
        atol = 10 ** - (7 + np.log10([refinement])[0])
        y_is_zero_or_close = set(np.around(X[np.isclose(self.f(X), 0.0, atol=atol)], 5))
        try:
            if method == 'newton':
                func = optimize.newton
                result = set(np.around([func(self.f, X[i]) for i, j in sign_changes], 5))
            else:
                func = getattr(optimize, method)
                result = set(np.around([func(self.f, X[i], X[j]) for i, j in sign_changes], 5))
            return result.union(y_is_zero_or_close)
        except RuntimeError:
            return []