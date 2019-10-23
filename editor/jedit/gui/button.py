import ipywidgets as w
from IPython.display import clear_output
import time

class Button:

    def __init__(self, description, button_style):
        self.button = w.Button(description=description,
                  button_style=button_style,
                  layout=w.Layout(height='auto', width='auto'))

    def get_widget(self):
        return self.button