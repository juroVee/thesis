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
        for Xi in self.function.get_parameter('derivatives'):
            derivatives = self.function.get_parameter('derivatives').get(Xi)
            for n in range(1, len(derivatives) + 1):
                if self.function.get_parameter('active_derivative' + str(n)):
                    X, dydx = derivatives.get(n)
                    color = self.function.get_parameter('derivative_color' + str(n))
                    linestyle = config['derivative']['linestyle']
                    linewidth = config['derivative']['linewidth']
                    self.ax.plot(X, dydx,
                                 color=color,
                                 linestyle=linestyle,
                                 linewidth=linewidth,
                                 zorder=2)

    def plot_zero_points(self):
        if self.function.get_parameter('zero_points_visible'):
            markersize = config['zero_points']['markersize']
            for x in self.function.get_parameter('zero_points_values'):
                self.ax.plot(x, 0, 'o', c=self.function.get_parameter('zero_points_color'), markersize=markersize, zorder=4)

    def plot_extremes(self):
        if self.function.get_parameter('extremes_visible'):
            markersize = config['extremes']['markersize']
            local_minima = self.function.get_parameter('local_minima')
            local_maxima = self.function.get_parameter('local_maxima')
            for x, y in local_minima + local_maxima:
                self.ax.plot(x, y, 'o', c=self.function.get_parameter('extremes_color'), markersize=markersize, zorder=4)

    def plot_inflex_points(self):
        if self.function.get_parameter('inflex_points_visible'):
            markersize = config['inflex_points']['markersize']
            f = self.function.get_parameter('f')
            for x in self.function.get_parameter('inflex_points_values'):
                self.ax.plot(x, f(x), 'o', c=self.function.get_parameter('inflex_points_color'), markersize=markersize, zorder=4)

    def plot_title(self):
        self.ax.set_title(self.function.get_parameter('latex'), y=1.06)