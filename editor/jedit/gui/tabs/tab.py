from ...config import config


class Tab:

    def __init__(self, name=None, main_window=None, sidebar=None, footer=None):
        self.name = name if name else 'Untitled Tab'
        self.main_window = main_window if main_window else []
        self.sidebar = sidebar if sidebar else []
        self.footer = footer if footer else []
        self.board_grid_rows = config['default_sizes']['board_grid_rows']
        self.board_grid_cols = config['default_sizes']['board_grid_cols']
        self.height = config['default_sizes']['board_grid_height']
        self.main_window_rows = config['default_sizes']['main_window_rows']
        self.main_window_cols = config['default_sizes']['main_window_cols']
