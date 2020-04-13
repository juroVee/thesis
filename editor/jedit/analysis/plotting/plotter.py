from .util import init_subplot
from ...config import config


class Plotter:

    def __init__(self, function, axes):
        self.function, self.ax = function, axes

    def plot_main_function(self):
        for line in self.function.get('lines'):
            X, Y = line.get_xdata(), line.get_ydata()
            init_subplot(self.ax)
            for param in self.function.parameters:
                try:
                    method = getattr(self.ax, 'set_' + param)
                    method(self.function.parameters[param])
                except AttributeError:
                    pass
            self.ax.grid(self.function.get('grid'))
            self.ax.plot(X, Y,
                         color=self.function.get('main_function_color'),
                         linestyle=config['main_function']['linestyle'],
                         linewidth=config['main_function']['linewidth'],
                         zorder=3)

    def plot_asymptotes(self):
        for line in self.function.get('asymptotes'):
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
        primes = self.function.get('derivatives')
        for i, X in enumerate(self.function.get('x_values')):
            key = f'X{i}'
            for n in range(1, len(primes[key]) + 1):
                if self.function.get('active_derivative' + str(n)):
                    dydx = primes[key].get(n)
                    color = self.function.get('derivative_color' + str(n))
                    linestyle = config['derivative']['linestyle']
                    linewidth = config['derivative']['linewidth']
                    self.ax.plot(X, dydx,
                                 color=color,
                                 linestyle=linestyle,
                                 linewidth=linewidth,
                                 zorder=2)

    def plot_zero_points(self):
        if self.function.get('zero_points_visible'):
            marker = config['zero_points']['marker']
            markersize = config['zero_points']['markersize']
            zorder = self.function.get('zero_points_zorder')
            dataset = self.function.get('zero_points_dataset')
            f = self.function.get('f')
            for xvals in dataset.values():
                self.ax.plot(xvals, f(xvals), marker, c=self.function.get('zero_points_color'),
                             markersize=markersize, zorder=zorder)

    def plot_extremes(self):
        if self.function.get('extremes_visible'):
            marker = config['extremes']['marker']
            markersize = config['extremes']['markersize']
            zorder = self.function.get('extremes_zorder')
            f = self.function.get('f')
            extremes = self.function.get('local_extrema')
            self.ax.plot(extremes, f(extremes), marker, c=self.function.get('extremes_color'), markersize=markersize, zorder=zorder)

    def plot_inflex_points(self):
        if self.function.get('inflex_points_visible'):
            marker = config['inflex_points']['marker']
            markersize = config['inflex_points']['markersize']
            zorder = self.function.get('inflex_points_zorder')
            f = self.function.get('f')
            inflex_points = self.function.get('inflex_points')
            self.ax.plot(inflex_points, f(inflex_points), marker, c=self.function.get('inflex_points_color'), markersize=markersize, zorder=zorder)


    def plot_intervals(self, op):
        if self.function.get(f'{op}_visible'):
            linestyle = config[op]['linestyle']
            linewidth = config[op]['linewidth']
            color = self.function.get(f'{op}_color')
            f = self.function.get('f')
            zorder = self.function.get(f'{op}_zorder')
            values = self.function.get(f'{op}_values')
            for interval in values:
                self.ax.plot(interval, f(interval), color=color, linestyle=linestyle, linewidth=linewidth,
                             zorder=zorder)

    def plot_title(self):
        self.ax.set_title(self.function.get('latex'), y=1.06)

    def plot_all(self):
        self.plot_main_function()
        self.plot_asymptotes()
        self.plot_derivative()
        self.plot_zero_points()
        self.plot_extremes()
        self.plot_inflex_points()
        for op in 'increasing', 'decreasing', 'concave_up', 'concave_down':
            self.plot_intervals(op)
        self.plot_title()
