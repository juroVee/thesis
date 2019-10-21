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
    def __init__(self, header=None, footer=None, left_sidebar=None, center=None, right_sidebar=None):
        self.header, self.footer = header, footer
        self.left_sidebar, self.center, self.right_sidebar = left_sidebar, center, right_sidebar

    def _calculate_grid_size(self, plot_width: int, plot_height: int) -> tuple:
        rows = plot_height + ceil(plot_height / 3)
        cols = plot_width + ceil(plot_width / 3)
        mid = ceil((7 * cols) / 10)
        return rows, cols, mid

    def app_layout(self) -> AppLayout:
        return AppLayout(header=self.header,
          left_sidebar=self.left_sidebar,
          center=self.center,
          right_sidebar=self.right_sidebar,
          footer=self.footer)

    def grid_space(self, plot_width: int, plot_height: int) -> GridspecLayout:
        rows, cols, mid = self._calculate_grid_size(plot_width, plot_height)
        print(f'r: {rows}, c: {cols}, m: {mid}')
        height_px = str(rows * 100) + "px"
        grid = GridspecLayout(rows, cols, height=height_px)
        grid[:, :mid] = self.center
        grid[:, mid:] = self.right_sidebar
        return grid


class Board:
    def __init__(self, fig, ax):
        self.plot = Plot(fig, ax)
        self._init_tabs()

    def _init_tabs(self):
        pw = self.plot.get_widget()
        pw_size_x, pw_size_y = self.plot.size
        self.tab1 = JTab(center=VBox(children=[pw]), right_sidebar=VBox(children=[freq_slider, range_slider]))
        self.tab2 = JTab(footer=VBox(children=[color_buttons]))
        self.tab3 = JTab(center=VBox())
        self.tabs = [self.tab1.grid_space(pw_size_x, pw_size_y), self.tab2.app_layout(), self.tab3.app_layout()]
        self.tab_names = ['Analysis', 'Settings', 'Info']
        self.tab = widgets.Tab(children=self.tabs)
        for i, name in enumerate(self.tab_names):
            self.tab.set_title(i, name)

    def get(self):
        return VBox(children=[self.tab])

