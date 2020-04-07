import yaml


class Config:

    def __init__(self):
        with open('jedit/config/config.yml', 'r') as yml:
            self.data = yaml.load(yml, Loader=yaml.FullLoader)

    def get_data(self):
        return self.data


# create instance alongside editor
config = Config().get_data()
