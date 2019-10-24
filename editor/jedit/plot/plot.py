import matplotlib.pyplot as plt
import ipywidgets as w
from .maux import *
from ..config.settings import DEFAULT_FUNCTIONS

def transform_title(title: str) -> str:
    start = title.find('$')
    end = title.rfind('$')
    return r'' + title[start:end + 1]

class Plot:
    """nacita hodnoty grafu nakresleneho uzivatelom
    a spravuje jeho parametre + spustanie (show)"""

    output = w.Output()

    def __init__(self, fig, ax):
        self.user_defined = not (fig is None and ax is None)
        self.user_data = []
        if self.user_defined:
            self._init_user_plot_data(fig, ax)
        else:
            function_name = 'y = x'
            function = DEFAULT_FUNCTIONS[function_name]['function']
            linspace = DEFAULT_FUNCTIONS[function_name]['linspace']
            self.defined_function = function, function_name, linspace
        self.color = 'C0'
        self.grid = False
        self.updated = False

    def _init_user_plot_data(self, fig, ax) -> None:
        self.fig = fig
        self.title = transform_title(ax.get_title())
        self.xdatas = [line.get_xdata() for line in ax.lines]
        self.ydatas = [line.get_ydata() for line in ax.lines]
        for child in ax.get_children():
            self.user_data.append(child)

    def plot_user_function(self) -> None:
        fig, ax = plt.subplots()
        fig.set_size_inches(6, 5.2)  # good: (6, 5)
        for X, Y in zip(self.xdatas, self.ydatas):
            init_subplot(ax)
            ax.set_title(self.title, loc='right', fontsize=10)
            # ax.set_aspect('equal')
            ax.grid(self.grid)
            ax.plot(X, Y, color=self.color)
        fig.show()

    def plot_function(self, function, function_name, linspace) -> None:
        fig, ax = plt.subplots()
        fig.set_size_inches(6, 5.2)
        X = linspace
        Y = function(X)
        init_subplot(ax)
        ax.set_title(function_name, loc='right', fontsize=10)
        # ax.set_aspect('equal')
        ax.grid(self.grid)
        ax.plot(X, Y, color=self.color)
        fig.show()

    def update(self) -> None:
        if self.updated:
            plt.close('all') # very important, possible memory exceeding instead
        if self.user_defined:
            self.plot_user_function()
        else:
            fun, name, linspace = self.defined_function
            self.plot_function(fun, name, linspace)