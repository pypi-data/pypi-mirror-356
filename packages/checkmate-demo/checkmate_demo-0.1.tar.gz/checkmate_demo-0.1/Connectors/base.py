from abc import ABC, abstractmethod

class BaseConnector(ABC):
    def __init__(self, config: dict):
        self.config = config
        self.engine = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def run_query(self, query: str):
        pass

    def close(self):
        if self.engine:
            self.engine.dispose()