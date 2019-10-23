import ipywidgets as w
from .outputs import log_output

GRID_ROWS = 16
PLOT_SIZE = 7

class Tab:
    """
    Fixed layout - GridspecLayout
    """
    def __init__(self, name=None, main_window=None, sidebar=None):
        self.name = name if name else 'Untitled Tab'
        self.main_window = main_window if main_window else []
        self.sidebar = sidebar if sidebar else []

    def get_grid_space(self) -> w.GridspecLayout:
        grid = w.GridspecLayout(GRID_ROWS, 10, height='620px')
        grid[:GRID_ROWS-1, :PLOT_SIZE] = w.VBox(children=self.main_window)
        grid[GRID_ROWS-1, :PLOT_SIZE] = w.VBox(children=[log_output],
                                               layout=w.Layout(height='auto'))
        for pos, item in self.sidebar:
            grid[pos, PLOT_SIZE:] = w.VBox(children=[item])
        return grid