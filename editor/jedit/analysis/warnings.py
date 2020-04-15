from queue import Queue

class WarningsManager:

    def __init__(self, logger):
        self.logger = logger
        self.data = Queue()

    def add(self, warnings_list):
        for warning in warnings_list:
            self.data.put(warning)

    def get(self):
        return self.data

    def print(self) -> None:
        """
        Method sends all the warnings generated during computations to logger object which prints them to the log
        """
        while not self.data.empty():
            warning = self.data.get()
            message = self.logger.new_message('upozornenie',
                                            správa=str(warning.message),
                                            kategória=str(warning.category),
                                            súbor=str(warning.filename))
            self.logger.write(message, warnings=True)
