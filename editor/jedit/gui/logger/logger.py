import os
from datetime import datetime

import ipywidgets as w
from IPython.display import clear_output

from .util import compose, LogStack
from ...config import config


class Logger:

    def __init__(self):
        self.outputs = {'main': w.Output(layout=w.Layout(overflow='auto')),
                        'mini': w.Output(),
                        'warnings': w.Output(layout=w.Layout(overflow='auto'))}
        self.log_stack = LogStack()
        self.warning_stack = LogStack()

    def set_order_oldest(self, value):
        self.log_stack.set_order(oldest=value)
        self.warning_stack.set_order(oldest=value)

    def write(self, message, main=False, mini=False, warnings=False, timer=False) -> None:
        """
        :param message: Message to be printed to log (better be 50 characters per line)
        :param main: printed to Log tab
        :param mini: printed to mini log under the analysis
        :param warnings: printed to Warnings tab
        :param timer: print if action is still being processed
        :return: None
        """
        if timer:
            with self.outputs['mini']:
                clear_output()
                print(message)
            return
        theme, kwargs = message
        out = f'[{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}]'
        if main:
            with self.outputs['main']:
                clear_output()
                message = compose(theme=theme, kwargs=kwargs)
                self.log_stack.push(out + message)
                self.log_stack.reveal()
        if mini and config['editor_settings']['footer_log'] == 'yes':
            with self.outputs['mini']:
                clear_output()
                message = compose(theme=theme, kwargs=kwargs, mini=True)
                print(message)
        if warnings:
            with self.outputs['warnings']:
                message = compose(theme=theme, kwargs=kwargs)
                self.warning_stack.push(out + message)
                self.warning_stack.reveal()

    def to_file(self) -> str:
        dir_name = 'editor_logs'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        file_name = str(datetime.now().strftime(f'{dir_name}/log-%d-%m-%Y-%H-%M-%S.txt'))
        with open(file_name, 'w') as file:
            self.log_stack.reveal(file=file)
        return file_name

    def get_widget(self, t=None) -> w.Output:
        return self.outputs[t]
