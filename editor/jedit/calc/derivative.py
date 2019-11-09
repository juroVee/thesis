from scipy.misc import derivative

def derivative_data(func, X):
    return X, derivative(func, X, dx=0.001)