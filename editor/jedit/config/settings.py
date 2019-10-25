import numpy as np
from ..plot.maux import smart_ticklabel

# disable interactive figure header
FIGURE_HEADER = False

# default functions list

DEFAULT_FUNCTION_SHOW = 'y = x^2'

DEFAULT_FUNCTIONS = {
    'y = x': {
        'function': lambda x: x,
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = x$'},
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
    'y = sin x': {
        'function': lambda x: np.sin(x),
        'linspace': np.linspace(-2*np.pi, 4*np.pi, 12*10+1),
        'latex': r'$y = \sin\ x$',
        'xticks_data': {'xticks':[n * np.pi / 2  for n in range(-4, 8+1)],
                       'xticklabels': [smart_ticklabel(n, r"\pi", 2) for n in range(-4, 8+1)]}},
    'y = |x|': {
        'function': lambda x: np.abs(x),
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = |x|$'},
    'y = e^x': {
        'function': lambda x: np.exp(x),
        'linspace': np.linspace(-10, 10, 101),
        'latex': r'$y = e^x$'},
    'y = log x': {
        'function': lambda x: np.log(x),
        'linspace': np.linspace(0.1, 10.1, 101),
        'latex': r'$y = \log\ x$'},
    'y = floor x': {
        'function': lambda x: np.floor(x),
        'linspace': np.linspace(-10, 10, 501),
        'latex': r'$y = x$'},
    'y = ceil x': {
        'function': lambda x: np.ceil(x),
        'linspace': np.linspace(-10, 10, 501),
        'latex': r'$y = x$'}
}
