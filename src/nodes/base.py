from abc import ABC, abstractmethod

# Basic Node to be inherited from.
class Node(ABC): 
    def __init__(self, config): 
        self.config = config

    @abstractmethod
    def set_model(self, provider, config): 
        ...

    @abstractmethod
    def run(self, state): 
        ...
