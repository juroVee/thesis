from ..settings import DERIV_COLORS
from .maux import init_subplot
from ..calculations import derivative_data, find_zero_points

IGNORED_PARAMS = ['title', 'lines', 'derivatives']

def plot_main_function(func, ax):
    number_of_lines = 0
    for line in func.parameters['lines']:
        X, Y = line.get_xdata(), line.get_ydata()
        number_of_lines += 1
        init_subplot(ax)
        for param in func.parameters.keys():
            if param not in IGNORED_PARAMS:
                method = getattr(ax, 'set_' + param)
                method(func.parameters[param])
        ax.grid(func.grid)
        ax.plot(X, Y,
                color=func.color if line.get_linestyle() == '-' else line.get_color(),
                label=func.latex if number_of_lines == 1 else '',
                linestyle=line.get_linestyle(),
                linewidth=line.get_linewidth())

def plot_derivative(func, ax):
    if len(func.parameters['derivatives']) > 0:
        number_of_lines = 0
        for X, Y in zip(func.x_values, func.y_values):
            number_of_lines += 1
            for n in func.parameters['derivatives']:
                _, dydx = derivative_data(func.function, X, n)
                quotes = n * "'"
                ax.plot(X, dydx, color=DERIV_COLORS[n], label=fr"f{quotes}(x)" if number_of_lines == 1 else '')
            # bottom, top = min((min(dydx), min(Y))), max((max(dydx), max(Y)))
            # ax.set_ylim(bottom, top)

def plot_zero_points(func, ax):
    ...

def plot_legend(ax):
    legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),
                       ncol=2)
    legend.get_frame().set_linewidth(0.0)
    legend.get_frame().set_facecolor('none')