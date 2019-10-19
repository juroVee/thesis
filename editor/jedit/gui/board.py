import ipywidgets as widgets
from ipywidgets import HBox, VBox
from .sliders import freq_slider, range_slider
from .buttons import color_buttons

class Board:
    def __init__(self):
        self.tab1 = self.tab2 = None
        self.init_tab1()
        self.init_tab2()

    def init_tab1(self):
        children = [freq_slider, range_slider]
        self.tab1 = VBox(children=children)

    def init_tab2(self):
        children = [color_buttons]
        self.tab1 = VBox(children=children)

    def data(self):
        children1 = [freq_slider, range_slider]
        tab1 = VBox(children=children1)
        children2 = [color_buttons]
        tab2 = VBox(children=children2)

        tab = widgets.Tab(children=[tab1, tab2])
        tab.set_title(0, 'Plot')
        tab.set_title(1, 'Settings')
        return VBox(children=[tab])
