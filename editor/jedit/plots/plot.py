import matplotlib.pyplot as plt
import numpy as np
from .maux import *
from ipywidgets import interactive, Output
from IPython.display import display
from math import floor, ceil

def f(X):
    return 2 * X ** 4 - 7 * X ** 3 + 5 * X ** 2 + 3 * X - 2

class Plot:
    """nacita hodnoty grafu nakresleneho uzivatelom
    a spravuje jeho parametre + spustanie (show)"""
    def __init__(self, fig, ax):
        self.data = {}
        self.fig, self.ax = fig, ax
        self.size = (7, 9) # temporary
        self.interactive_fields = False
        self._resize()

    def _resize(self):
        # default DPI in Matplotlib = 100
        grid_height = 400 if self.interactive_fields else 500
        x, y = self.size
        print(f'original: {self.size}')
        factor = (y * 100) / grid_height
        self.size = x / factor, y / factor
        print(f'resized: {self.size}')

    def plot_function(self):
        fig, ax = plt.subplots()
        size_x, size_y = self.size
        fig.set_size_inches(6, 5)
        X = np.linspace(-0.70, 2.20, 29 * 100 + 1)  # výber hodnôt nezávislej premennej pre zaujímavú časť grafu
        Y = f(X)
        init_subplot(ax)
        ax.set_title(r"Graf funkcie $y = 2x^4-7x^3+5x^2+3x-2$")  # pomenovanie diagramu
        ax.set_aspect('equal')
        plt.ioff()
        ax.plot(X, Y)
        fig.show()

    def get_widget(self) -> interactive:
        widget = interactive(self.plot_function)
        #widget.layout = {'border': '5px solid black'}
        return widget




