import ipywidgets as w
from .slider import freq_slider
from .tab import Tab, GRID_ROWS
from ..plot import Plot
from .buttons import reset_button, grid_toggle_button, box
from .outputs import print_output, log_output
from .observer import Observer
from IPython.display import clear_output, display
import time

class Board:

    grid_toggle = w.ToggleButtons(
        options=['On', 'Off'],
        description='Grid:',
        disabled=False,
        button_style='',  # 'success', 'info', 'warning', 'danger' or ''
        tooltips=['Description of slow', 'Description of fast']
    )



    def __init__(self, fig, ax):
        self.plot = Plot(fig, ax)
        self.plot_widget = self.plot.get_widget()
        self.init_tabs()
        self.observer = Observer(self)
        self.observer.start()

    def init_tabs(self):
        tab1 = Tab(name='Analysis',
                 main_window=[self.plot.get_widget()],
                 sidebar=[(0, freq_slider),
                          (1, freq_slider),
                          (2, freq_slider),
                          (3, box),
                          (GRID_ROWS-1, reset_button)]
                 )
        tab2 = Tab(name='Settings')
        tab3 = Tab(name='Info')
        self.tab_parent= w.Tab(children=[t.get_grid_space() for t in (tab1, tab2, tab3)])
        for i, tab in enumerate((tab1, tab2, tab3)):
            self.tab_parent.set_title(i, tab.name)

    def get_widget(self) -> w.VBox:
        return w.VBox(children=[self.tab_parent])



