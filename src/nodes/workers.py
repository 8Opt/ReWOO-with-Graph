"""
    The Worker receives the plan and executes the tools in sequence.
"""
from langchain_community.tools.tavily_search import TavilySearchResults

from src.models import LanguageModel
from src.nodes.base import Node


class TavilyEngine(Node): 
    def __init__(self, config):
        self.engine = self.set_model(provider=config['provider'], 
                                     config=config['settings'])

    def set_model(self, provider, config):
        engine = TavilySearchResults(**config)
        return engine
    
    def run(self, state):
        return self.engine.invoke(state)
    
class LLMEngine(Node): 
    def __init__(self, config): 
        self.engine = self.set_model(provider=config['provider'], 
                                     config=config['settings'])

    def set_model(self, provider, config):
        model = LanguageModel.from_prebuilt(provider=provider, 
                                            config=config)
        return model
    
    def run(self, state):
        return self.model.invoke(state)

class Workers: 

    @staticmethod
    def call_engine(name, config): 
        match name: 
            case "search": 
                return TavilyEngine(config)
            case "llm": 
                return LLMEngine(config)