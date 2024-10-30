from abc import ABC, abstractmethod
import logging
from typing import List
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_core.output_parsers import JsonOutputParser
from ..models.schemas import EmailStructure
from ..llm.options import LLMOption
from ..llm.factory import FACTORY_MAP

class EmailGenerator(ABC):
    @abstractmethod
    def generate(self, content: List[str], purpose: str, prompt: str) -> EmailStructure:
        pass

class LangChainEmailGenerator(EmailGenerator):
    def __init__(self, llm_option: LLMOption):
        self.logger = logging.getLogger(__name__ + ".LangChainEmailGenerator")
        factory_class = FACTORY_MAP.get(llm_option.provider)
        if not factory_class:
            raise ValueError(f"Unsupported LLM provider: {llm_option.provider}")
        
        factory = factory_class(llm_option.model_id)
        self.llm = factory.create_llm()
        self.parser = JsonOutputParser(pydantic_object=EmailStructure)
        self.logger.info(f"Initialized with {llm_option.name}")

    def _create_chain(self, custom_prompt: str):
        email_prompt = PromptTemplate(
            template="""
            Purpose: {purpose}\n\n
            Use the information below to craft the email:\n\n
            {text}\n\n
            """+custom_prompt+"""\n\n
            Also, provide a suitable subject line for this cold email.
            {format_instructions}
            COLD EMAIL:
            """,
            input_variables=["text", "purpose"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        refine_prompt = PromptTemplate(
            template="""
            Purpose: {purpose}\n\n

            We have provided a draft cold email: {existing_answer}
            Refine the email based on additional context below to make it more compelling or leave it as is if not needed.
            ------------
            {text}
            ------------
            Refine the cold email in English based on the new context. If the new context is not useful, return the original cold email.
            {format_instructions}
            """,
            input_variables=["existing_answer", "text", "purpose"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        return load_summarize_chain(
            llm=self.llm,
            chain_type="refine",
            question_prompt=email_prompt,
            refine_prompt=refine_prompt,
            return_intermediate_steps=False,
            verbose=True
        )

    def generate(self, content: List[str], purpose: str, prompt: str) -> EmailStructure:
        try:
            self.logger.info("Generating email content")
            chain = self._create_chain(prompt)
            result = chain.invoke({
                "input_documents": content,
                "purpose": purpose
            })
            
            parsed_result = self.parser.parse(result["output_text"])
            print(parsed_result)
            self.logger.info("Successfully generated email content")
            return parsed_result
        except Exception as e:
            self.logger.error(f"Error generating email: {str(e)}")
            raise