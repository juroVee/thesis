# external modules
import ipywidgets as w
from IPython.display import clear_output
from datetime import datetime

# project-level modules
from ..config import config

class Logger:

    def __init__(self):
        self.outputs = {'main': w.Output(), 'mini': w.Output(), 'warnings': w.Output()}
        self.log_backup = []

    def write(self, message, main=False, mini=False, warnings=False):
        """
        :param message: Message to be printed to log (better be 50 characters per line)
        :param main: printed to Log tab
        :param mini: printed to mini log under the plot
        :param warnings: printed to Warnings tab
        :return: None
        """
        if config['editor_settings']['footer_log'] != 'yes':
            return
        out = f'[{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}] {message}'
        if main:
            with self.outputs['main']:
                print(out)
                self.log_backup.append(out)
        if mini:
            with self.outputs['mini']:
                clear_output()
                print(message)
        if warnings:
            with self.outputs['warnings']:
                print(out)

    def to_file(self):
        with open(str(datetime.now().strftime("log-%d-%m-%Y-%H-%M-%S.txt")), 'w') as file:
            for log in self.log_backup:
                file.write(log)

    def get_widget(self, t=None):
        return self.outputs[t]