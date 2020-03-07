# external modules
import ipywidgets as w
from IPython.display import clear_output
from datetime import datetime

# project-level modules
from ..config import config


def compose(theme, kwargs, mini=False):
    if mini:
        return f'{theme}: {kwargs}'
    result = f'\n\tpopis akcie: {theme}'
    for arg, val in kwargs.items():
        result += '\n\t'
        if type(val) == list:
            result += f'{arg}: [\n\t   '
            result += ',\n\t   '.join(map(str, val)) + '\n\t]'
        else:
            result += f'{arg}: {val}'
    return result


class Logger:

    def __init__(self):
        self.outputs = {'main': w.Output(layout=w.Layout(overflow='auto')),
                        'mini': w.Output(),
                        'warnings': w.Output(layout=w.Layout(overflow='auto'))}
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
        theme, kwargs = message
        out = f'[{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}]'
        if main:
            with self.outputs['main']:
                message = compose(theme=theme, kwargs=kwargs)
                print(out + message)
                self.log_backup.append(out)
        if mini:
            with self.outputs['mini']:
                clear_output()
                message = compose(theme=theme, kwargs=kwargs, mini=True)
                print(message)
        if warnings:
            with self.outputs['warnings']:
                message = compose(theme=theme, kwargs=kwargs)
                print(out + message)

    def to_file(self):
        with open(str(datetime.now().strftime("log-%d-%m-%Y-%H-%M-%S.txt")), 'w') as file:
            for log in self.log_backup:
                file.write(log)

    def get_widget(self, t=None):
        return self.outputs[t]