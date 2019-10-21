import ipywidgets as widgets
from math import floor, ceil
from ipywidgets import VBox, AppLayout, Output, Button, Layout, GridspecLayout
from .sliders import freq_slider, range_slider
from .buttons import color_buttons
from ..plots import Plot

import matplotlib.pyplot as plt

def create_expanded_button(description, button_style):
    return Button(description=description, button_style=button_style, layout=Layout(height='auto', width='auto'))

header_button = create_expanded_button('Title', 'success')
# left_button = create_expanded_button('Left', 'info')
# center_button = create_expanded_button('Center', 'warning')
# right_button = create_expanded_button('Right', 'info')
# footer_button = create_expanded_button('Footer', 'success')

class JTab:
    """Fixed layout - AppLayout (header, footer, left, right sidebar and center"""
    def __init__(self, name=None, header=None, footer=None, left_sidebar=None, center=None, right_sidebar=None):
        self.name = name
        self.header, self.footer = header, footer
        self.left_sidebar, self.center, self.right_sidebar = left_sidebar, center, right_sidebar

    def app_layout(self) -> AppLayout: # not used yet
        return AppLayout(header=self.header,
          left_sidebar=self.left_sidebar,
          center=self.center,
          right_sidebar=self.right_sidebar,
          footer=self.footer)

    def grid_space(self) -> GridspecLayout:
        grid = GridspecLayout(10, 10, height='600px')
        grid[:, :7] = self.center
        grid[:, 7:] = self.right_sidebar
        #grid[:2, :7] = header_button
        return grid



class Board:
    def __init__(self, fig, ax):
        self.plot = Plot(fig, ax)
        self._init_tabs()

    def _init_tabs(self):
        pw = self.plot.get_widget()
        tabs = [
            JTab(name='Analysis',
                 center=VBox(children=[pw]),
                 right_sidebar=VBox(children=[freq_slider] * 5)
                 ),
            JTab(name='Settings',
                 center=VBox(children=[color_buttons]),
                 right_sidebar=VBox()
                 ),
            JTab(name='Info',
                 center=VBox(),
                 right_sidebar=VBox()
                 )
        ]
        self.tab = widgets.Tab(children=[t.grid_space() for t in tabs])
        for i, tab in enumerate(tabs):
            self.tab.set_title(i, tab.name)

    def get(self):
        return VBox(children=[self.tab])

