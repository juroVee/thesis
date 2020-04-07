import numpy as np


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
