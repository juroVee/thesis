import numpy as np
from .plot.maux import smart_ticklabel

# DISABLE DEFAULT INTERACTIVE HEADER FROM MATPLOTLIB
FIGURE_HEADER = False

# SET DEFAULT FUNCTION NAMES
LINEAR = 'y = x'
QUADRATIC = 'y = x^2'
CUBIC = 'y = x^3'
SQRT = 'y = \u221Ax\u0305'
E = 'y = e^x'
LOG = 'y = log x'
SIN = 'y = sin x'
COS = 'y = cos x'

# SET DEFAULT FUNCTIONS DEFINITIONS (USING NUMPY)
DEFAULT_FUNCTIONS = {
    LINEAR: {
        'f': lambda x: x,
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = x$'},
    QUADRATIC: {
        'f': lambda x: np.power(x, 2),
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = x^2$'},
    CUBIC: {
        'f': lambda x: np.power(x, 3),
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = x^3$'},
    SQRT: {
        'f': lambda x: np.sqrt(x),
        'linspace': np.linspace(0.1, 20, 101),
        'latex': r'$y = \sqrt{x}$'},
    E: {
        'f': lambda x: np.exp(x),
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = e^x$'},
    LOG: {
        'f': lambda x: np.log(x),
        'linspace': np.linspace(0.1, 10.1, 101),
        'latex': r'$y = \log\ x$'},
    SIN: {
        'f': lambda x: np.sin(x),
        'linspace': np.linspace(-2 * np.pi, 4 * np.pi, 12 * 10 + 1),
        'latex': r'$y = \sin\ x$',
        'xticks_data': {'xticks': [n * np.pi / 2 for n in range(-4, 8 + 1)],
                        'xticklabels': [smart_ticklabel(n, r"\pi", 2) for n in range(-4, 8 + 1)]}},
    COS: {
        'f': lambda x: np.cos(x),
        'linspace': np.linspace(-2 * np.pi, 4 * np.pi, 12 * 10 + 1),
        'latex': r'$y = \cos\ x$',
        'xticks_data': {'xticks': [n * np.pi / 2 for n in range(-4, 8 + 1)],
                        'xticklabels': [smart_ticklabel(n, r"\pi", 2) for n in range(-4, 8 + 1)]}},
}

# DEFAULT DERIVATION COLORS
DERIV_COLORS = {1: '#ff8647', 2: '#39ff33', 3: '#7b6cef'}

# SET FIRST FUNCTION TO SHOW IF USER FUNCTION NOT PROVIDED
DEFAULT_FUNCTION_TO_SHOW = LINEAR