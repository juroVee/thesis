import yaml


class Settings:

    def __init__(self):
        with open('jedit/settings/settings.yml', 'r') as yml:
            self.data = yaml.load(yml, Loader=yaml.FullLoader)

    def get_data(self):
        return self.data


# create instance alongside editor
settings = Settings().get_data()