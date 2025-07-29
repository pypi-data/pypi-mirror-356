from abc import ABC, abstractmethod

class BaseCheck(ABC):
    def __init__(self, connector, config):
        self.connector = connector
        self.config = config

    @abstractmethod
    def run(self):
        pass