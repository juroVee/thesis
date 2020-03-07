# package-level modules
from .gui import Board
from .gui import Logger
from .util import NotSupportedException, hide_interactive_toolbars, check_parameters
from .config import config

# external modules
from matplotlib import get_backend
import matplotlib.pyplot as plt
from IPython.display import display, clear_output


class Editor:

    def __init__(self):
        self.board = None
        self.logger = Logger()

    def run(self, **params):
        if not config['editor_settings']['figure_header'] == 'yes':
            hide_interactive_toolbars()
        if 'inline' in get_backend():
            raise NotSupportedException('Clause %matplotlib inline is not supported. Please use %matplotlib notebook.')
        for t in 'main', 'mini', 'warnings':
            self.logger.get_widget(t).clear_output()
        self.board = Board(check_parameters(params, self.logger), self.logger)
        manager = self.board.get_manager_object()
        observer = self.board.get_observer_object()
        display(self.board.get_widget())

        # width, height = config['plot_parameters']['width'], config['plot_parameters']['height']
        # fig, ax = plt.subplots()
        # fig.set_size_inches(width, height)

        manager.update_plot(main_function=True,
                                    derivatives=True,
                                    zero_points=True,
                                    extremes=True,
                                    inflex_points=True,
                                    monotonic=True,
                                    convex=True
                                    )
        observer.write_warnings()

# run instance after importing editor
editor = Editor()


