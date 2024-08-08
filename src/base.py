from abc import ABC, abstractmethod
from typing import List, TypedDict


class ReWOO(TypedDict):
    task: str
    plan_string: str
    steps: List
    results: dict
    result: str

class BaseFoundationModel(ABC): 

    @staticmethod
    @abstractmethod
    def from_pretrained(provider:str, config:dict): 
        ...