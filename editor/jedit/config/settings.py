import numpy as np

# disable interactive figure header
FIGURE_HEADER = False

# default functions list

DEFAULT_FUNCTIONS = {
    'y = x': {
        'function': lambda x: x,
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = x$'},
    'y = |x|': {
        'function': lambda x: np.abs(x),
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = |x|$'},
    'y = x^2': {
        'function': lambda x: np.power(x, 2),
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = x^2$'},
    'y = \u221Ax\u0305': {
        'function': lambda x: np.sqrt(x),
        'linspace': np.linspace(0.1, 20, 101),
        'latex': r'$y = \sqrt{x}$'},
    'y = x^3': {
        'function': lambda x: np.power(x, 3),
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = x^3$'},
    'y = sin(x)': {
        'function': lambda x: np.sin(x),
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = \sin\ x$'}
}