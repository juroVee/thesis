# external modules
import os
import ipywidgets as w
from IPython.display import clear_output
from datetime import datetime
import numpy as np

# project-level modules
from ..config import config


def compose(theme, kwargs, mini=False):
    if mini:
        return f'{theme}: {kwargs}'
    result = f'\n\tpopis akcie: {theme}'
    for arg, val in kwargs.items():
        result += '\n\t'
        if type(val) == list or type(val) == np.ndarray:
            if len(val) > 0:
                result += f'{arg}: [\n\t   '
                result += ',\n\t   '.join(map(str, val)) + '\n\t]'
            else:
                result += f'{arg}: []'
        else:
            result += f'{arg}: {val}'
    return result


class Logger:

    class LogStack:

        def __init__(self, oldest=False):
            self.oldest = oldest
            self.data = []

        def set_order(self, oldest):
            self.oldest = oldest

        def push(self, item):
            self.data.append(item)

        def reveal(self, file=None):
            if self.oldest:
                for value in self.data:
                    print(value) if file is None else print(value, file=file)
            else:
                for i in range(len(self.data) - 1, -1, -1):
                    print(self.data[i]) if file is None else print(self.data[i], file=file)

        def is_empty(self):
            return len(self.data) == 0


    def __init__(self):
        self.outputs = {'main': w.Output(layout=w.Layout(overflow='auto')),
                        'mini': w.Output(),
                        'warnings': w.Output(layout=w.Layout(overflow='auto'))}
        self.log_stack = self.LogStack()
        self.warning_stack = self.LogStack()

    def set_order_oldest(self, value):
        self.log_stack.set_order(oldest=value)
        self.warning_stack.set_order(oldest=value)

    def write(self, message, main=False, mini=False, warnings=False, timer=False):
        """
        :param message: Message to be printed to log (better be 50 characters per line)
        :param main: printed to Log tab
        :param mini: printed to mini log under the plot
        :param warnings: printed to Warnings tab
        :param timer: print if action is still being processed
        :return: None
        """
        if timer:
            with self.outputs['mini']:
                clear_output()
                print(message)
            return
        if config['editor_settings']['footer_log'] != 'yes':
            return
        theme, kwargs = message
        out = f'[{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}]'
        if main:
            with self.outputs['main']:
                clear_output()
                message = compose(theme=theme, kwargs=kwargs)
                self.log_stack.push(out + message)
                self.log_stack.reveal()
        if mini:
            with self.outputs['mini']:
                clear_output()
                message = compose(theme=theme, kwargs=kwargs, mini=True)
                print(message)
        if warnings:
            with self.outputs['warnings']:
                message = compose(theme=theme, kwargs=kwargs)
                self.warning_stack.push(out + message)
                self.warning_stack.reveal()

    def to_file(self):
        dir_name = 'editor_logs'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        file_name = str(datetime.now().strftime(f'{dir_name}/log-%d-%m-%Y-%H-%M-%S.txt'))
        with open(file_name, 'w') as file:
            self.log_stack.reveal(file=file)
        return file_name

    def get_widget(self, t=None):
        return self.outputs[t]