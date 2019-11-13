from matplotlib.lines import Line2D
from .function import Function
from ..config import DEFAULT_FUNCTIONS, DEFAULT_FUNCTION_TO_SHOW
from ..util import transform_title

class FunctionCarousel:

    def __init__(self, user_data: dict):
        self.functions = {}
        self._load_default_functions()
        self.current_function = self.functions[DEFAULT_FUNCTION_TO_SHOW]
        if user_data is not None:
            self._load_user_function(user_data)

    def _load_default_functions(self) -> None:
        for name, data in DEFAULT_FUNCTIONS.items():
            function, X, latex = data['function'], data['linspace'], data['latex']
            func = Function([X], [function(X)], function, name, latex)
            lines = [Line2D(X, function(X))]
            func.set_parameter('lines', lines)
            func.set_parameter('title', name)
            func.set_parameter('aspect', 'auto')
            if 'xticks_data' in data.keys():
                func.set_parameter('xticks', data['xticks_data']['xticks'])
                func.set_parameter('xticklabels', data['xticks_data']['xticklabels'])
            self.functions[name] = func

    def _load_user_function(self, user_data: dict) -> None:
        fig, ax, function = user_data['figure'], user_data['axis'], user_data['function']
        X = [xvals for xvals in user_data['xvals']]
        Y = [function(xvals) for xvals in X]
        self.current_function = self.functions['user function'] = Function(
            X = X,
            Y = Y,
            function=function,
            name='user function',
            latex=transform_title(ax.get_title())
        )
        self.current_function.set_parameter('title', ax.get_title())
        self.current_function.set_parameter('aspect', ax.get_aspect())
        self.current_function.set_parameter('xticks', ax.get_xticks())
        self.current_function.set_parameter('yticks', ax.get_yticks())
        if ax.get_xticklabels()[0].get_text() != '':
            self.current_function.set_parameter('xticklabels', ax.get_xticklabels())
        if ax.get_yticklabels()[0].get_text() != '':
            self.current_function.set_parameter('yticklabels', ax.get_yticklabels())
        self.current_function.set_parameter('xlim', ax.get_xlim())
        self.current_function.set_parameter('ylim', ax.get_ylim())
        lines = [line for line in ax.get_lines() if line.get_xdata() != [] and line.get_ydata() != []]
        self.current_function.set_parameter('lines', lines)

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