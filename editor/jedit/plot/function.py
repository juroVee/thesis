import matplotlib.pyplot as plt
import numpy as np
from .maux import init_subplot
from ..calc import derivative_data

IGNORED_PARAMS = ['title', 'lines']

class Function:

    def __init__(self, X, Y, function, name, latex):
        self.x_values, self.y_values = X, Y
        self.function, self.name, self.latex = function, name, latex

        # plot params shared
        self.grid = False
        self.color = 'C0'
        self.derivative_n = 0

        self.parameters = {}

        self.original_x_values = X
        self.refinement = 0.

    def __repr__(self):
        return f'Function(name={self.name})'

    def plot(self) -> None:
        for xval in self.x_values:
            print(f'(DEBUG) Refinement: {self.refinement} Partitions: {len(xval)}')
        fig, ax = plt.subplots()
        fig.set_size_inches(6, 5)
        number_of_lines = 0
        for line in self.parameters['lines']:
            X, Y = line.get_xdata(), line.get_ydata()
            number_of_lines += 1
            init_subplot(ax)
            for param in self.parameters.keys():
                if param not in IGNORED_PARAMS:
                    method = getattr(ax, 'set_' + param)
                    method(self.parameters[param])
            ax.grid(self.grid)
            ax.plot(X, Y,
                    color=self.color if line.get_linestyle() == '-' else line.get_color(),
                    label=self.latex if number_of_lines == 1 else '',
                    linestyle=line.get_linestyle(),
                    linewidth=line.get_linewidth())


        if self.derivative_n > 0:
            number_of_lines = 0
            for X, Y in zip(self.x_values, self.y_values):
                number_of_lines += 1
                _, dydx = derivative_data(self.function, X, self.derivative_n)
                quotes = self.derivative_n * "'"
                ax.plot(X, dydx, color='#ff8647', label=fr"f{quotes}(x)" if number_of_lines == 1 else '')
                # bottom, top = min((min(dydx), min(Y))), max((max(dydx), max(Y)))
                # ax.set_ylim(bottom, top)
            else:
                # TODO
                pass
        legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),
                      ncol=2)
        legend.get_frame().set_linewidth(0.0)
        legend.get_frame().set_facecolor('none')
        fig.show()

    def set_parameter(self, name, value):
        self.parameters[name] = value

    def set_grid(self, value=False) -> None:
        self.grid = value

    def set_derivative_plot(self, value=0) -> None:
        self.derivative_n = value

    def set_color(self, value='C0') -> None:
        self.color = value

    def set_refinement(self, value=0.) -> None:
        self.refinement = value
        new_x_values = []
        for xval in self.original_x_values:
            minima, maxima = min(xval), max(xval)
            partitions = len(xval)
            new_partitions = int(partitions + partitions * self.refinement)
            new_x_values.append(np.linspace(minima, maxima, new_partitions))
        self.x_values = new_x_values

    def get_name(self) -> str:
        return self.name

    def get_latex(self) -> str:
        return self.latex