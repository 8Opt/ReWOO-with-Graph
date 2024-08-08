"""
    The Planner prompts an LLM to generate a plan in the form of a task list. 
    The arguments to each task are strings that may contain special variables (#E{0-9}+) that are 
    used for variable substitution from other task results.
"""

from langchain_core.prompts import ChatPromptTemplate

from src.prompts.base import PLANNER_PROMPT
from src.models import LanguageModel
from src.nodes.base import Node

class Planner(Node): 
    def __init__(self, config):
        super().__init__(config=config)
        self.model = self.set_model(provider=config['provider'], 
                                    config=config['settings'])
        
    def set_model(self, provider, config):
        model = LanguageModel.from_prebuilt(provider, config)
        prompt_template = ChatPromptTemplate.from_messages([("user", PLANNER_PROMPT)])
        planner = prompt_template | model
        return planner
    
    def run(self, state):
        result = self.model.invoke(state)
        return result
    
