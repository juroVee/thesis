from .function import Function
from ..config import FUNCTIONS, DEFAULT_FUNCTION
from ..util import transform_title

class FunctionCarousel:

    def __init__(self, user_data):
        self._load_default_functions()
        self.current_function = self.functions[DEFAULT_FUNCTION]
        self.user_defined = all(var is not None for var in user_data)
        if self.user_defined:
            self.user_data = user_data
            self._load_user_function()

    def _load_default_functions(self):
        self.functions = {}
        for name, data in FUNCTIONS.items():
            function = data['function']
            X = data['linspace']
            latex = data['latex']
            self.functions[name] = Function([X], [function(X)], name, latex)
            if 'xticks_data' in data.keys():
                self.functions[name].xticks = data['xticks_data']['xticks']
                self.functions[name].xticks_labels = data['xticks_data']['xticklabels']

    def _load_user_function(self):
        fig, ax, X, Y = self.user_data
        X = [line.get_xdata() for line in ax.lines]
        Y = [line.get_ydata() for line in ax.lines]
        latex = transform_title(ax.get_title())
        self.functions['user function'] = Function(X=X, Y=Y, name='user function', latex=latex)
        self.current_function = self.functions['user function']
        self.current_function.set_aspect(ax.get_aspect())
        self.current_function.set_xtics(ax.get_xticks())
        if ax.get_xticklabels()[0].get_text() != '':
            self.current_function.set_xtics_labels(ax.get_xticklabels())

    def __getitem__(self, function_name):
        return self.functions[function_name]

    def __repr__(self):
        return 'FunctionCarousel(\n\t' + '\n\t'.join(self.functions) + '\n)'

    def get_all(self):
        return self.functions.values()

    def get_current(self):
        return self.current_function

    def set_current(self, function):
        self.current_function = function

    def has_user_function(self):
        return 'user function' in self.functions.keys()