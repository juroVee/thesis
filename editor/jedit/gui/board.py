import ipywidgets as w
from .sliders import freq_slider
from .buttons import button_reset, visible_log
from ..plots import Plot

GRID_ROWS = 16

class JTab:
    """
    Fixed layout - GridspecLayout
    """
    def __init__(self, name=None, main_window=None, sidebar=None):
        self.name = name if name else 'Untitled Tab'
        self.main_window = main_window if main_window else []
        self.sidebar = sidebar if sidebar else []

    def get_grid_space(self) -> w.GridspecLayout:
        grid = w.GridspecLayout(GRID_ROWS, 10, height='620px')
        grid[:GRID_ROWS-1, :7] = w.VBox(children=self.main_window)
        grid[GRID_ROWS-1, :7] = w.VBox(children=[visible_log], layout=w.Layout(height='auto'))
        for pos, item in self.sidebar:
            grid[pos, 7:] = w.VBox(children=[item])
        return grid

class Board:

    def __init__(self, fig, ax):
        self.plot = Plot(fig, ax)
        self._init_tabs()

    def _init_tabs(self):
        pw = self.plot.get_widget()
        tabs = [
            JTab(name='Analysis',
                 main_window=[pw],
                 sidebar=[(0, freq_slider), # i in <0, GRID_ROWS-1>
                          (1, freq_slider),
                          (2, freq_slider),
                          (GRID_ROWS-1, button_reset)]
                 ),
            JTab(name='Settings'),
            JTab(name='Info')
        ]
        self.tab = w.Tab(children=[t.get_grid_space() for t in tabs])
        for i, tab in enumerate(tabs):
            self.tab.set_title(i, tab.name)

    def get(self) -> w.VBox:
        return w.VBox(children=[self.tab])