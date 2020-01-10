# external modules
import ipywidgets as w
from datetime import datetime

class Logger:

    output = w.Output()

    def __init__(self):
        self.log_backup = []

    def write(self, message):
        with self.output:
            out = f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} -> {message}'
            print(out)
            self.log_backup.append(out)

    def to_file(self):
        with open(str(datetime.now().strftime("log-%d-%m-%Y-%H-%M-%S.txt")), 'w') as file:
            for log in self.log_backup:
                file.write(log)

    def get_widget(self):
        return self.output