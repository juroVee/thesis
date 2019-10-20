from os import path

import ipywidgets as widgets
from ipywidgets import VBox, AppLayout, Button, Layout
from .sliders import freq_slider, range_slider
from .buttons import color_buttons


def create_expanded_button(description, button_style):
    return Button(description=description, button_style=button_style, layout=Layout(height='auto', width='auto'))

header_button = create_expanded_button('Title', 'success')
left_button = create_expanded_button('Left', 'info')
center_button = create_expanded_button('Center', 'warning')
right_button = create_expanded_button('Right', 'info')
footer_button = create_expanded_button('Footer', 'success')

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "..", "resources", "img.gif"))
image = widgets.Image(value=open(filepath, "rb").read(), format='png', width=400, height=400)

tab1 = AppLayout(header=None,
          left_sidebar=None,
          center=image,
          right_sidebar=VBox(children=[freq_slider, range_slider]),
          footer=footer_button)
tab2 = VBox(children=[color_buttons])
tab3 = VBox()

class Board:
    def __init__(self):
        self.tabs = [tab1, tab2, tab3]
        self.tab_names = ['Analysis', 'Settings', 'Info']
        self.tab = widgets.Tab(children=self.tabs)
        for i, name in enumerate(self.tab_names):
            self.tab.set_title(i, name)

    def get(self):
        return VBox(children=[self.tab])

