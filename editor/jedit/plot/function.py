import matplotlib.pyplot as plt
from .maux import init_subplot

class Function:

    def __init__(self, X, Y, name, latex):
        self.X, self.Y, self.name, self.latex = X, Y, name, latex

        # plot params shared
        self.grid = False
        self.color = 'C0'
        self.aspect = 'auto'

        # plot params individual
        self.xticks = None
        self.xticks_labels = None

    def __repr__(self):
        return f'Function(name={self.name})'

    def plot(self):
        fig, ax = plt.subplots()
        fig.set_size_inches(6, 5.2)
        for X, Y in zip(self.X, self.Y):
            init_subplot(ax)
            ax.set_title(self.latex, loc='right', fontsize=10)
            ax.set_aspect(self.aspect)
            if self.xticks is not None:
                ax.set_xticks(self.xticks)
            if self.xticks_labels is not None:
                ax.set_xticklabels(self.xticks_labels)
            ax.grid(self.grid)
            ax.plot(X, Y, color=self.color)
        fig.show()

    def set_xtics(self, xtics):
        self.xticks = xtics

    def set_xtics_labels(self, xtics_labels):
        self.xticks_labels = xtics_labels

    def set_grid(self, value=False):
        self.grid = value

    def set_aspect(self, value='auto'):
        self.aspect = value

    def set_color(self, value='C0'):
        self.color = value

    def get_name(self):
        return self.name

    def get_latex(self):
        return self.latex