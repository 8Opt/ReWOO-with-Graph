"""
    The Solver receives the full plan and generates the final response based on the responses of the tool calls from the worker.
"""

from langchain_core.prompts import ChatPromptTemplate

from src.prompts.base import SOLVER_PROMPT
from src.models import LanguageModel
from src.nodes.base import Node

class Solver(Node): 
    def __init__(self, config):
        super().__init__(config=config)
        self.model = self.set_model(provider=config['provider'], 
                                    config=config['settings'])
        
    def set_model(self, provider, config):
        model = LanguageModel.from_prebuilt(provider, config)
        prompt_template = ChatPromptTemplate.from_messages([("user", SOLVER_PROMPT)])
        sovler = prompt_template | model
        return sovler
    
    def run(self, state):
        result = self.model.invoke(state)
        return result