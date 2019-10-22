import matplotlib.pyplot as plt
from .maux import *
from ipywidgets import interactive


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
        # self.test(fig, ax)

    def test(self, fig, ax):
        print(fig)
        print(ax)
        print(fig)
        print(ax.get_children())
        print(self.xdatas)
        print(self.ydatas)

    def _init_user_plot_data(self, fig, ax):
        self.fig = fig
        self.title = transform_title(ax.get_title())
        self.xdatas = [line.get_xdata() for line in ax.lines]
        self.ydatas = [line.get_ydata() for line in ax.lines]
        for child in ax.get_children():
            self.user_data.append(child)

    def plot_function(self):
        fig, ax = plt.subplots()
        fig.set_size_inches(6, 5)
        for X, Y in zip(self.xdatas, self.ydatas):
            init_subplot(ax)
            ax.set_title(self.title)
            ax.set_aspect('equal')
            ax.plot(X, Y)
        fig.show()

    def get_widget(self) -> interactive:
        widget = interactive(self.plot_function)
        #widget.layout = {'border': '5px solid black'}
        return widget




