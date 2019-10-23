import ipywidgets as w

class Output:

    def __init__(self):
        self.output = w.Output()

    def get_widget(self):
        return self.output