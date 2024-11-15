from abc import ABC, abstractmethod


class ConnectionPoolInterface(ABC):
    """
    an interface for the ConnectionPool class.
    """
    @abstractmethod
    def _connect(self):
        pass


    @abstractmethod
    def _disconnect(self):
        pass

    
    @abstractmethod
    def runsql(self):
        pass


    @abstractmethod
    def select(self):
        pass
