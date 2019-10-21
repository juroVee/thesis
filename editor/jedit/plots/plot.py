import matplotlib.pyplot as plt
from ipywidgets import interactive, Output
from math import floor, ceil

class Plot:
    """nacita hodnoty grafu nakresleneho uzivatelom
    a spravuje jeho parametre + spustanie (show)"""
    def __init__(self, fig, ax):
        self.data = {}
        self.fig, self.ax = fig, ax
        self.size = (7, 9) # temporary
        self._resize()

    def _resize(self):
        x, y = self.size
        print(f'original: {self.size}')
        x, y = floor((3 * x) / 4), floor((3 * y) / 4)
        self.size = x, y
        print(f'resized: {self.size}')

    def plot_function(self):
        fig, ax = plt.subplots()
        size_x, size_y = self.size
        fig.set_size_inches(size_x, size_y)
        ax.plot([1, 2, 3], [4, 5, 6])
        fig.show()

    def get_widget(self) -> interactive:
        widget = interactive(self.plot_function)
        widget.layout = {'border': '5px solid black'}
        return widget




