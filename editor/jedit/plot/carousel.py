from .function import Function
from ..config import FUNCTIONS, DEFAULT_FUNCTION
from ..util import transform_title

class FunctionCarousel:

    def __init__(self, user_data: tuple):
        self._load_default_functions()
        self.current_function = self.functions[DEFAULT_FUNCTION]
        self.user_defined = all(var is not None for var in user_data)
        if self.user_defined:
            self.user_data = user_data
            self._load_user_function()

    def _load_default_functions(self) -> None:
        self.functions = {}
        for name, data in FUNCTIONS.items():
            function = data['function']
            X = data['linspace']
            latex = data['latex']
            self.functions[name] = Function([X], [function(X)], function, name, latex)
            if 'xticks_data' in data.keys():
                self.functions[name].xticks = data['xticks_data']['xticks']
                self.functions[name].xticks_labels = data['xticks_data']['xticklabels']

    def _load_user_function(self) -> None:
        fig, ax, function, X_vals = self.user_data
        X = [xvals for xvals in X_vals]
        Y = [function(xvals) for xvals in X]
        latex = transform_title(ax.get_title())
        self.functions['user function'] = Function(X=X, Y=Y, function=function, name='user function', latex=latex)
        self.current_function = self.functions['user function']
        self.current_function.set_aspect(ax.get_aspect())
        self.current_function.set_xtics(ax.get_xticks())
        if ax.get_xticklabels()[0].get_text() != '':
            self.current_function.set_xtics_labels(ax.get_xticklabels())

    def __getitem__(self, function_name: str):
        return self.functions[function_name]

    def __repr__(self):
        return 'FunctionCarousel(\n\t' + '\n\t'.join(self.functions) + '\n)'

    def get_all(self) -> dict.values:
        return self.functions.values()

    def get_current(self) -> Function:
        return self.current_function

    def set_current(self, function: Function) -> None:
        self.current_function = function

    def has_user_function(self) -> bool:
        return 'user function' in self.functions.keys()