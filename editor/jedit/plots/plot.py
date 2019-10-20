import matplotlib.pyplot as plt
from ipywidgets import interactive, Output

def plot_function():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    fig.show()

class Plot:
    """nacita hodnoty grafu nakresleneho uzivatelom
    a spravuje jeho parametre + spustanie (show)"""
    def __init__(self, fig, ax):
        self.data = {}
        self.fig, self.ax = fig, ax

    def get_widget(self):
        return interactive(plot_function)




