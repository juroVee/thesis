import matplotlib.pyplot as plt
import ipywidgets as w
from .function import Function
from ..config import DEFAULT_FUNCTIONS, DEFAULT_FUNCTION_SHOW

def transform_title(title: str) -> str:
    start = title.find('$')
    end = title.rfind('$')
    return r'' + title[start:end + 1]

def load_functions() -> dict:
    functions = {}
    for name, data in DEFAULT_FUNCTIONS.items():
        X = data['linspace']
        func = data['function']
        latex = data['latex']
        functions[name] = Function(X=[X], Y=[func(X)], name=name, latex=latex)
        if 'xticks_data' in data.keys():
            functions[name].xticks = data['xticks_data']['xticks']
            functions[name].xticks_labels = data['xticks_data']['xticklabels']

    return functions

class Plot:

    output = w.Output()

    def __init__(self, fig, ax):
        self.functions = load_functions()
        self.current_function = None
        self.user_defined = False
        self.updated = False
        if not (fig is None and ax is None): # if user defined
            self.user_defined = True
            X = [line.get_xdata() for line in ax.lines] # toto vsetko do nejakeho loadingu #TODO
            Y = [line.get_ydata() for line in ax.lines]
            latex = transform_title(ax.get_title())
            name = transform_title(latex)
            self.functions['user defined'] = Function(X=X, Y=Y, name=name, latex=latex)
            self.current_function = self.functions['user defined']
            self.current_function.set_xtics(ax.get_xticks())
            if ax.get_xticklabels()[0].get_text() != '':
                self.current_function.set_xtics_labels(ax.get_xticklabels())

        else:
            self.current_function = self.functions[DEFAULT_FUNCTION_SHOW]

    def is_user_defined(self):
        return self.user_defined

    def update(self) -> None:
        if self.updated:
            plt.close('all') # very important, possible memory exceeding
        self.current_function.plot()