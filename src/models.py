from src.base import BaseFoundationModel

class LanguageModel(BaseFoundationModel): 
    @staticmethod
    def from_prebuilt(provider:str, config:dict): 
        match provider: 
            case 'gemini': 
                try:
                    from langchain_google_genai import ChatGoogleGenerativeAI
                except ImportError as e: 
                    raise e
                return ChatGoogleGenerativeAI(**config)
            case "ollama": 
                try:
                    from langchain_community.chat_models import ChatOllama
                except ImportError as e: 
                    raise e
                return ChatOllama(**config)
            case "groq": 
                try:
                    from langchain_groq import ChatGroq
                except ImportError as e: 
                    raise e
                return ChatGroq(**config)