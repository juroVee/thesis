import matplotlib.pyplot as plt
import ipywidgets as w
from .maux import *
from IPython.display import display, clear_output

def transform_title(title: str) -> str:
    start = title.find('$')
    end = title.rfind('$')
    return r'' + title[start:end + 1]

class Plot:
    """nacita hodnoty grafu nakresleneho uzivatelom
    a spravuje jeho parametre + spustanie (show)"""

    output = w.Output()

    def __init__(self, fig, ax):
        self.user_data = []
        self._init_user_plot_data(fig, ax)
        self.color = 'C0'
        self.grid = False
        self.updated = False

    def _init_user_plot_data(self, fig, ax):
        self.fig = fig
        self.title = transform_title(ax.get_title())
        self.xdatas = [line.get_xdata() for line in ax.lines]
        self.ydatas = [line.get_ydata() for line in ax.lines]
        for child in ax.get_children():
            self.user_data.append(child)

    def plot_function(self):
        if self.updated:
            plt.close('all') # very important, possible memory exceeding instead
        plt.ioff()
        fig, ax = plt.subplots()
        plt.ion()
        fig.set_size_inches(6, 5.2) # good: (6, 5)
        for X, Y in zip(self.xdatas, self.ydatas):
            init_subplot(ax)
            ax.set_title(self.title, loc='right', fontsize=10)
            #ax.set_aspect('equal')
            ax.grid(self.grid)
            ax.plot(X, Y, color=self.color)
        display(self.output)
        with self.output:
            clear_output()
            display(fig)

    def get_widget(self) -> w.interactive:
        widget = w.interactive(self.plot_function)
        widget.layout = {'border': '3px solid black'}
        return w.interactive(self.plot_function)