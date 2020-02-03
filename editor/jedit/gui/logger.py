# external modules
import ipywidgets as w
from IPython.display import clear_output
from datetime import datetime

# project-level modules
from ..config import config

class Logger:

    output = w.Output()
    output_mini = w.Output()
    output_warnings = w.Output()

    def __init__(self):
        self.log_backup = []

    def write(self, message):
        with self.output:
            out = f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} -> {message}'
            print(out)
            self.log_backup.append(out)

    def write_mini(self, message):
        """
        :param message: Message to be printed to log (better be 50 characters per line)
        :return: None
        """
        if config['editor_settings']['footer_log'] != 'yes':
            return
        with self.output_mini:
            clear_output()
            print(f'[LATEST] {message}')
            # time.sleep(3)

    def write_warning(self, message):
        with self.output_warnings:
            out = f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} -> {message}'
            print(out)

    def to_file(self):
        with open(str(datetime.now().strftime("log-%d-%m-%Y-%H-%M-%S.txt")), 'w') as file:
            for log in self.log_backup:
                file.write(log)

    def get_widget(self, t=None):
        if t == 'warnings':
            return self.output_warnings
        elif t == 'mini':
            return self.output_mini
        else:
            return self.output