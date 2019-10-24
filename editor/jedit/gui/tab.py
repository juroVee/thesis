import ipywidgets as w

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
        grid = w.GridspecLayout(GRID_ROWS, 10, height='560px')
        grid[:GRID_ROWS, :PLOT_SIZE] = w.VBox(children=self.main_window)
        for pos, item in self.sidebar:
            grid[pos, PLOT_SIZE:] = w.VBox(children=[item])
        return grid