from IPython.display import display, clear_output
from .buttons import box

class Observer:

    def __init__(self, board):
        self.loaded_board = board

    def changed(self, b):
        val = b['new']
        if val:
            self.loaded_board.plot.grid = True
        else:
            self.loaded_board.plot.grid = False
        self.loaded_board.plot.updated = True
        self.loaded_board.plot_widget = self.loaded_board.plot.get_widget()
        self.loaded_board.init_tabs()
        display(self.loaded_board.plot.get_widget())

    def start(self):
        box.observe(self.changed, 'value')

