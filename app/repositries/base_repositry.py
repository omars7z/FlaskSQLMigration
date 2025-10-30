from abc import ABC, abstractmethod

class BaseRepositry(ABC):
        
    @abstractmethod
    def get(self):
        pass
    
    @abstractmethod
    def create(self, data):
        pass
    
    @abstractmethod
    def update(self, id, data):
        pass
    
    @abstractmethod
    def delete(self, id):
        pass
    