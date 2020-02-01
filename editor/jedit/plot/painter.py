# project-level modules
from ..config import config

# package-level modules
from .maux import init_subplot, smart_ticklabel

class Painter:

    def __init__(self, function, axes):
        self.function, self.ax = function, axes

    def plot_main_function(self):
        for line in self.function.get_parameter('lines'):
            X, Y = line.get_xdata(), line.get_ydata()
            init_subplot(self.ax)
            for param in self.function.parameters:
                try:
                    method = getattr(self.ax, 'set_' + param)
                    method(self.function.parameters[param])
                except AttributeError:
                    pass
            self.ax.grid(self.function.get_parameter('grid'))
            self.ax.plot(X, Y,
                         color=self.function.get_parameter('main_function_color'),
                         linestyle=config['main_function']['linestyle'],
                         linewidth=config['main_function']['linewidth'],
                         zorder=3)

    def plot_asymptotes(self):
        for line in self.function.get_parameter('asymptotes'):
            X, Y = line.get_xdata(), line.get_ydata()
            linestyle = config['asymptote']['linestyle']
            linewidth = config['asymptote']['linewidth']
            color = config['asymptote']['color']
            self.ax.plot(X, Y,
                         color=color,
                         linestyle=linestyle,
                         linewidth=linewidth,
                         zorder=1)

    def plot_derivative(self):
        for n in range(1, len(self.function.get_parameter('derivatives')) + 1):
            if self.function.get_parameter('active_derivative' + str(n)):
                X, dydx = self.function.get_parameter('derivatives').get(n)
                color = self.function.get_parameter('derivative_color' + str(n))
                linestyle = config['derivative']['linestyle']
                linewidth = config['derivative']['linewidth']
                self.ax.plot(X, dydx,
                             color=color,
                             linestyle=linestyle,
                             linewidth=linewidth,
                             zorder=2)

    def plot_zero_points(self):
        if self.function.get_parameter('zero_points_method') != 'none':
            markersize = config['zero_points']['markersize']
            for x in self.function.get_parameter('zero_points_values'):
                self.ax.plot(x, 0, 'o', c=self.function.get_parameter('zero_points_color'), markersize=markersize, zorder=4)

    def plot_title(self):
        self.ax.set_title(self.function.get_parameter('latex'), y=1.06)