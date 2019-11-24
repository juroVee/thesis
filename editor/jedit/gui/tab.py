import ipywidgets as w

GRID_ROWS = 18
PLOT_SIZE = 7

class Tab:
    """
    Fixed layout - GridspecLayout
    """
    def __init__(self, name=None, main_window=None, sidebar=None, footer=None):
        self.name = name if name else 'Untitled Tab'
        self.main_window = main_window if main_window else []
        self.sidebar = sidebar if sidebar else []
        self.footer = footer if footer else []

    def get_grid_space(self) -> w.GridspecLayout:
        grid = w.GridspecLayout(GRID_ROWS, 10, height='600px')
        grid[:GRID_ROWS-2, :PLOT_SIZE] = w.VBox(children=self.main_window)
        for pos, item in self.sidebar:
            grid[pos, PLOT_SIZE:] = w.VBox(children=[item])
        for pos, item in self.footer:
            grid[GRID_ROWS - 2 + pos, :PLOT_SIZE] = w.VBox(children=[item])
        return grid