# external modules
from scipy.misc import derivative
from scipy import optimize
import numpy as np

# project-level modules
from ..config import config

class Calculator:

    def __init__(self, f):
        self.f = f


class DerivativeCalculator(Calculator):

    def __init__(self, f):
        super().__init__(f)

    def derive(self, X, n):
        order = n + 1 if n % 2 == 0 else n + 2
        return X, derivative(self.f, X, dx=0.001, n=n, order=order)


class ZeroPointsCalculator(Calculator):

    def __init__(self, f):
        super().__init__(f)
        self.rounding = int(config['zero_points']['round'])

    def _find_sign_changes(self, X):
        fX = self.f(X)
        fX[fX == 0.] = 0.
        return np.where(np.diff(np.signbit(fX)))[0]

    def _process(self, X, found_points) -> set:
        touching_zero = set(X[self.f(X) == 0.0])
        rounded = np.around(found_points, self.rounding)
        rounded += 0.
        return touching_zero.union(set(rounded))

    def zero_points(self, X, method='newton'):
        indexes = self._find_sign_changes(X)
        sign_changes = list(zip(indexes, np.add(1, indexes)))
        try:
            if method == 'newton':
                func = optimize.newton
                found = [func(self.f, X[i]) for i, j in sign_changes]
            else:
                func = getattr(optimize, method)
                found = [func(self.f, X[i], X[j]) for i, j in sign_changes]
            return self._process(X, found)
        except RuntimeError:
            return self._process(X, [])



