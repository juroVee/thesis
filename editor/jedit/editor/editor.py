from IPython.display import display
from matplotlib import get_backend

from .exceptions import NotSupportedException
from .util import hide_interactive_toolbars, check_parameters
from ..gui import Board, Logger
from ..settings import settings


class Editor:

    def __init__(self):
        self.board = None
        self.logger = Logger()

    def run_instance(self, **params):
        if not settings['editor_settings']['interactive_elements'] == 'yes':
            hide_interactive_toolbars()
        if 'inline' in get_backend():
            raise NotSupportedException('Clause %matplotlib inline is not supported. Please use %matplotlib notebook.')
        for t in 'main', 'mini', 'warnings':
            self.logger.get_widget(t).clear_output()
        self.board = Board(check_parameters(params, self.logger), self.logger)
        function_manager = self.board.get_object('function_manager')
        display(self.board.get_widget())
        function_manager.update_plot(main_function=True, derivatives=True, zero_points=True,
                                     extremes=True, inflex_points=True, monotonic=True, concave=True)
