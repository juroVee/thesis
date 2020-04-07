def logger_message(theme, **kwargs):
    return theme, kwargs


class Configuration:

    def __init__(self):
        self.configuration = {}

    def get(self):
        return self.configuration

    def __getitem__(self, item):
        return self.configuration[item]

    def save(self, parameter, value):
        self.configuration[parameter] = value
