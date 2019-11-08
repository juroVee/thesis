import numpy as np
from ..plot.maux import smart_ticklabel

# disable interactive figure header
FIGURE_HEADER = False

# default functions list

LINEAR = 'y = x'
QUADTRATIC = 'y = x^2'
CUBIC = 'y = x^3'
SQRT = 'y = \u221Ax\u0305'
E = 'y = e^x'
LOG = 'y = log x'
SIN = 'y = sin x'

DEFAULT_FUNCTION = LINEAR

FUNCTIONS = {
    LINEAR: {
        'function': lambda x: x,
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = x$'},
    QUADTRATIC: {
        'function': lambda x: np.power(x, 2),
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = x^2$'},
    CUBIC: {
        'function': lambda x: np.power(x, 3),
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = x^3$'},
    SQRT: {
        'function': lambda x: np.sqrt(x),
        'linspace': np.linspace(0.1, 20, 101),
        'latex': r'$y = \sqrt{x}$'},
    E: {
        'function': lambda x: np.exp(x),
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = e^x$'},
    LOG: {
        'function': lambda x: np.log(x),
        'linspace': np.linspace(0.1, 10.1, 101),
        'latex': r'$y = \log\ x$'},
    SIN: {
        'function': lambda x: np.sin(x),
        'linspace': np.linspace(-2 * np.pi, 4 * np.pi, 12 * 10 + 1),
        'latex': r'$y = \sin\ x$',
        'xticks_data': {'xticks': [n * np.pi / 2 for n in range(-4, 8 + 1)],
                        'xticklabels': [smart_ticklabel(n, r"\pi", 2) for n in range(-4, 8 + 1)]}},
}
