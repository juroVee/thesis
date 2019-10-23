import matplotlib.pyplot as plt
import ipywidgets as w
from .maux import *


def transform_title(title: str) -> str:
    start = title.find('$')
    end = title.rfind('$')
    return r'' + title[start:end + 1]

class Plot:
    """nacita hodnoty grafu nakresleneho uzivatelom
    a spravuje jeho parametre + spustanie (show)"""
    def __init__(self, fig, ax):
        self.user_data = []
        self._init_user_plot_data(fig, ax)
        self.color = 'C0'

    def _init_user_plot_data(self, fig, ax):
        self.fig = fig
        self.title = transform_title(ax.get_title())
        self.xdatas = [line.get_xdata() for line in ax.lines]
        self.ydatas = [line.get_ydata() for line in ax.lines]
        for child in ax.get_children():
            self.user_data.append(child)

    def plot_function(self):
        fig, ax = plt.subplots()
        fig.set_size_inches(6, 5) # good: (6, 5)
        for X, Y in zip(self.xdatas, self.ydatas):
            init_subplot(ax)
            ax.set_title(self.title, loc='right', fontsize=10)
            #ax.set_aspect('equal')
            ax.plot(X, Y, color=self.color)
        fig.show()

    def get_widget(self) -> w.interactive:
        widget = w.interactive(self.plot_function)
        #widget.layout = {'border': '5px solid black'}
        return widget