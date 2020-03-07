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
            zorder = self.function.get_parameter('zero_points_zorder')
            for x in self.function.get_parameter('zero_points_values'):
                self.ax.plot(x, 0, 'o', c=self.function.get_parameter('zero_points_color'), markersize=markersize, zorder=zorder)

    def plot_extremes(self):
        if self.function.get_parameter('extremes_visible'):
            markersize = config['extremes']['markersize']
            minX = self.function.get_parameter('local_minima_xvals')
            maxX = self.function.get_parameter('local_maxima_xvals')
            minY = self.function.get_parameter('local_minima_yvals')
            maxY = self.function.get_parameter('local_maxima_yvals')
            zorder = self.function.get_parameter('extremes_zorder')
            self.ax.plot(minX, minY, 'o', c=self.function.get_parameter('extremes_color'), markersize=markersize, zorder=zorder)
            self.ax.plot(maxX, maxY, 'o', c=self.function.get_parameter('extremes_color'), markersize=markersize, zorder=zorder)

    def plot_inflex_points(self):
        if self.function.get_parameter('inflex_points_visible'):
            markersize = config['inflex_points']['markersize']
            X = self.function.get_parameter('inflex_points_xvals')
            Y = self.function.get_parameter('inflex_points_yvals')
            zorder = self.function.get_parameter('inflex_points_zorder')
            self.ax.plot(X, Y, 'o', c=self.function.get_parameter('inflex_points_color'), markersize=markersize, zorder=zorder)

    def plot_analysis(self, op):
        if self.function.get_parameter(f'{op}_visible'):
            linestyle = config[op]['linestyle']
            linewidth = config[op]['linewidth']
            color = self.function.get_parameter(f'{op}_color')
            f = self.function.get_parameter('f')
            zorder = self.function.get_parameter(f'{op}_zorder')
            for X in self.function.get_parameter(f'{op}_xvals'):
                self.ax.plot(X, f(X), color=color, linestyle=linestyle, linewidth=linewidth, zorder=zorder)

    def plot_title(self):
        self.ax.set_title(self.function.get_parameter('latex'), y=1.06)