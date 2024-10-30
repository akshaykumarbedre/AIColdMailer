from abc import ABC, abstractmethod
import os
from typing import Dict, Type
from langchain.base_language import BaseLanguageModel
from langchain_groq import ChatGroq
import streamlit as st

class LLMFactory(ABC):
    def __init__(self, model_id: str):
        self.model_id = model_id
    
    @abstractmethod
    def create_llm(self) -> BaseLanguageModel:
        pass

class GroqFactory(LLMFactory):
    def create_llm(self) -> BaseLanguageModel:
        return ChatGroq(
            model_name=self.model_id,
            # groq_api_key=os.getenv("GROQ_API_KEY"),
            groq_api_key=st.secrets['GROQ_API_KEY'],#used to deploy in streamlit cloud
            temperature=0.7,
            
        )

# Map of factory classes
FACTORY_MAP: Dict[str, Type[LLMFactory]] = {
    "groq": GroqFactory,
}