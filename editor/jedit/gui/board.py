import ipywidgets as w
from ..analysis import FunctionManager
from .tabs import AnalysisTab, LogTab, WarningTab
from .menu import MainMenu, Observer


class Board:

    def __init__(self, user_params, logger):
        if 'config' in user_params:
            self.user_config = user_params['config']
        self.logger = logger
        self.function_manager = FunctionManager(user_params)
        self.main_menu = MainMenu()
        tabs = [AnalysisTab(board=self),
                LogTab(board=self),
                WarningTab(board=self)]
        self.tab_parent = w.Tab(children=[tab.get_widget() for tab in tabs])
        for i, tab in enumerate(tabs):
            self.tab_parent.set_title(i, tab.name)
        self.observer = Observer(self)
        self.observer.start()

    def get_object(self, object_name):
        if hasattr(self, object_name):
            return getattr(self, object_name)

    def get_widget(self) -> w.VBox:
        return w.VBox(children=[self.tab_parent])
