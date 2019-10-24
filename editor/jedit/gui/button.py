import ipywidgets as w

class Button:

    def __init__(self, description, button_style, board):
        self.button = w.Button(description=description,
                  button_style=button_style,
                  layout=w.Layout(height='auto', width='auto'))
        self.board = board

    def get_widget(self):
        return self.button