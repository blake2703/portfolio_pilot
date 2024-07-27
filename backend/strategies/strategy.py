from abc import abstractmethod, ABC

class Strategy(ABC):
    
    def add_ta(self):
        pass
    
    def buy_signal(self, data):
        pass
    
    def sell_signal(self, data):
        pass