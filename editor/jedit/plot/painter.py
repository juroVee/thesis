# project-level modules
from ..settings import DERIV_COLORS

# package-level modules
from .maux import init_subplot


class Painter:

    IGNORED_PARAMS = ['title', 'lines', 'derivatives']

    def __init__(self, function, axes):
        self.function, self.ax = function, axes
        self.calculator = self.function.get_calculator()

    def plot_main_function(self):
        number_of_lines = 0
        for line in self.function.parameters['lines']:
            X, Y = line.get_xdata(), line.get_ydata()
            number_of_lines += 1
            init_subplot(self.ax)
            for param in self.function.parameters.keys():
                if param not in self.IGNORED_PARAMS:
                    method = getattr(self.ax, 'set_' + param)
                    method(self.function.parameters[param])
            self.ax.grid(self.function.grid)
            self.ax.plot(X, Y,
                    color=self.function.color if line.get_linestyle() == '-' else line.get_color(),
                    label=self.function.latex if number_of_lines == 1 else '',
                    linestyle=line.get_linestyle(),
                    linewidth=line.get_linewidth())

    def plot_derivative(self):
        if len(self.function.parameters['derivatives']) > 0:
            number_of_lines = 0
            for X, Y in zip(self.function.x_values, self.function.y_values):
                number_of_lines += 1
                for n in self.function.parameters['derivatives']:
                    _, dydx = self.calculator.derive(X, n)
                    quotes = n * "'"
                    color = self.function.get_derivative_color(n)
                    self.ax.plot(X, dydx, color=color, label=fr"f{quotes}(x)" if number_of_lines == 1 else '')

    def plot_zero_points(self):
        if self.function.zero_points != 'none':
            for X, Y in zip(self.function.x_values, self.function.y_values):
                zero_points = self.calculator.zero_points(X, self.function.zero_points)
                self.function.zero_points_values = list(zero_points)
                if self.function.zero_points_values is not None:
                    for x in self.function.zero_points_values:
                        self.ax.plot(x, 0, 'ko', c=self.function.zero_points_color)

    def plot_title(self):
        self.ax.set_title(self.function.get_latex())