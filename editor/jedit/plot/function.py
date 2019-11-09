import matplotlib.pyplot as plt
from .maux import init_subplot
from ..calc import derivative_data

class Function:

    def __init__(self, X, Y, function, name, latex):
        self.x_values, self.y_values = X, Y
        self.function, self.name, self.latex = function, name, latex

        # plot params shared
        self.grid = False
        self.color = 'C0'
        self.aspect = 'auto'
        self.derivative_plot = False

        # plot params individual
        self.xticks = None
        self.xticks_labels = None

    def __repr__(self):
        return f'Function(name={self.name})'

    def plot(self) -> None:
        fig, ax = plt.subplots()
        fig.set_size_inches(6, 5.2)
        number_of_lines = 0
        for X, Y in zip(self.x_values, self.y_values):
            number_of_lines += 1
            init_subplot(ax)
            #ax.set_title(self.latex, loc='right', fontsize=10)
            ax.set_aspect(self.aspect)
            if self.xticks is not None:
                ax.set_xticks(self.xticks)
            if self.xticks_labels is not None:
                ax.set_xticklabels(self.xticks_labels)
            ax.grid(self.grid)
            ax.plot(X, Y, color=self.color, label=self.latex if number_of_lines == 1 else '')
        if self.derivative_plot and number_of_lines == 1:
            X, Y = self.x_values[0], self.y_values[0]
            _, dx = derivative_data(self.function, X)
            ax.plot(X, dx, color='#ff8647', label=fr"f'(x)")
            bottom, top = min(Y), max(Y)
            ax.set_ylim(bottom, top)
        else:
            # TODO
            pass
        legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),
                      ncol=2)
        legend.get_frame().set_linewidth(0.0)
        legend.get_frame().set_facecolor('none')
        fig.show()

    def set_xtics(self, xtics) -> None:
        self.xticks = xtics

    def set_xtics_labels(self, xtics_labels) -> None:
        self.xticks_labels = xtics_labels

    def set_grid(self, value=False) -> None:
        self.grid = value

    def set_derivative_plot(self, value=False) -> None:
        self.derivative_plot = value

    def set_aspect(self, value='auto') -> None:
        self.aspect = value

    def set_color(self, value='C0') -> None:
        self.color = value

    def get_name(self) -> str:
        return self.name

    def get_latex(self) -> str:
        return self.latex