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
                    self.ax.plot(X, dydx, color=DERIV_COLORS[n], label=fr"f{quotes}(x)" if number_of_lines == 1 else '')

    def plot_zero_points(self):
        ...

    def plot_legend(self):
        legend = self.ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),
                           ncol=2)
        legend.get_frame().set_linewidth(0.0)
        legend.get_frame().set_facecolor('none')