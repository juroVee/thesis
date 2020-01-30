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

    def get_widget(self) -> w.GridspecLayout:
        board_grid_rows = config['default_sizes']['board_grid_rows']
        board_grid_cols = config['default_sizes']['board_grid_cols']
        height = config['default_sizes']['board_grid_height']
        main_window_rows = config['default_sizes']['main_window_rows']
        main_window_cols = config['default_sizes']['main_window_cols']
        grid = w.GridspecLayout(board_grid_rows, board_grid_cols, height=height)
        grid[:main_window_rows, :main_window_cols] = w.VBox(children=self.main_window)
        for pos, item in self.sidebar:
            grid[pos, main_window_cols:] = w.VBox(children=[item])
        grid[main_window_rows:, :main_window_cols] = w.VBox(children=self.footer)
        return grid


class AnalysisTab(Tab):

    def __init__(self, board=None):
        plot = board.get_plot_object()
        gui_manager = board.get_gui_manager_object()
        gui_elements = gui_manager.get_elements()
        logger = board.get_logger_object()
        super().__init__(name='Analysis',
                   main_window=[plot.get_widget()],
                   sidebar=[(0, gui_elements['hbox']['function']),
                            (1, gui_elements['dropdown']['grid']),
                            (3, gui_elements['hbox']['derivative1']),
                            (4, gui_elements['hbox']['derivative2']),
                            (5, gui_elements['hbox']['derivative3']),
                            (7, gui_elements['dropdown']['refinement']),
                            (8, gui_elements['hbox']['zero_points'])
                            #(9, gui_elements['dropdown']['zp_derivatives_signs'])
                            ],
                    footer=[logger.get_widget(mini=True)]
                   )


class SettingsTab(Tab):

    def __init__(self, board=None):
        super().__init__(name='Settings')


class LogTab(Tab):

    def __init__(self, board=None):
        logger = board.get_logger_object()
        super().__init__(name='Log', main_window=[logger.get_widget()])


class InfoTab(Tab):

    def __init__(self, board=None):
        super().__init__(name='Info')