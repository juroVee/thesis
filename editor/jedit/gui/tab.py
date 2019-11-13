import ipywidgets as w
import os

here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'logo.png')

GRID_ROWS = 18
PLOT_SIZE = 7
LOGO_BOX_ROWS = 2

logo_image = w.Image(
    value=open(filename, 'rb').read(),
    format='png',
    width=60,
    height=60
)

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

        logo_box = w.GridspecLayout(1, 5, height='100px')
        logo_box[:, -1:] = logo_image
        grid[:LOGO_BOX_ROWS, PLOT_SIZE:] = w.HBox(children=[logo_box])

        for pos, item in self.sidebar:
            grid[LOGO_BOX_ROWS + pos, PLOT_SIZE:] = w.VBox(children=[item])

        for pos, item in self.footer:
            grid[GRID_ROWS - 2 + pos, :PLOT_SIZE] = w.VBox(children=[item])

        return grid