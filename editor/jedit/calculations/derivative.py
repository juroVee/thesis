from scipy.misc import derivative

def derivative_data(func, X, n):
    order = n + 1 if n % 2 == 0 else n + 2
    return X, derivative(func, X, dx=0.001, n=n, order=order)