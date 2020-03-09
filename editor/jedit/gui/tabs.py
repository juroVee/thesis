# external modules
import ipywidgets as w

# project-level modules
from ..config import config


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


class AnalysisTab(Tab):

    def __init__(self, board=None):
        manager = board.get_manager_object()
        gui_manager = board.get_gui_manager_object()
        logger = board.get_logger_object()
        logger_mini_tab = w.Tab(children=[logger.get_widget(t='mini')], layout=w.Layout(height='100%'))
        logger_mini_tab.set_title(0, 'Posledná zmena')
        super().__init__(name='Analýza',
                   main_window=[manager.get_plot_widget()],
                   sidebar=[gui_manager.get_main_menu()],
                    footer=[logger_mini_tab]
                   )

    def get_widget(self) -> w.GridspecLayout:
        grid = w.GridspecLayout(self.board_grid_rows, self.board_grid_cols, height=self.height)
        grid[:self.main_window_rows, :self.main_window_cols] = w.VBox(children=self.main_window)
        grid[:self.main_window_rows, self.main_window_cols:] = w.VBox(children=self.sidebar)
        grid[self.main_window_rows:, :self.board_grid_cols] = w.VBox(children=self.footer)
        return grid


class LogTab(Tab):

    def __init__(self, board=None):
        logger = board.get_logger_object()
        super().__init__(name='Výstupy', main_window=[logger.get_widget(t='main')])

    def get_widget(self) -> w.GridspecLayout:
        grid = w.GridspecLayout(self.board_grid_rows, self.board_grid_cols, height=self.height)
        grid[:self.board_grid_rows, :self.board_grid_cols] = w.VBox(children=self.main_window)
        return grid


class WarningTab(Tab):

    def __init__(self, board=None):
        logger = board.get_logger_object()
        super().__init__(name='Upozornenia', main_window=[logger.get_widget(t='warnings')])

    def get_widget(self) -> w.GridspecLayout:
        grid = w.GridspecLayout(self.board_grid_rows, self.board_grid_cols, height=self.height)
        grid[:self.board_grid_rows, :self.board_grid_cols] = w.VBox(children=self.main_window)
        return grid