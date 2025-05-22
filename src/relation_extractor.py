from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
# from langchain.core.output_parsers.json import JsonOutputParser
from langchain_core.output_parsers.json import JsonOutputParser
# from langchain.pydantic_v1 import  Field #BaseModel,
from pydantic import BaseModel, Field
# from pydantic.v1 import BaseModel
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import json
import os
from langchain.prompts.chat import (ChatPromptTemplate,HumanMessagePromptTemplate,SystemMessagePromptTemplate)

class ExtractedInfo(BaseModel):
    head: str = Field(description="extracted first or head entity like Microsoft, Apple, John")
    head_type: str = Field(description="type of the extracted head entity like person, company, etc")
    relation: str = Field(description="relation between the head and the tail entities")
    tail: str = Field(description="extracted second or tail entity like Microsoft, Apple, John")
    tail_type: str = Field(description="type of the extracted tail entity like person, company, etc")

class RelationExtractor:
    def __init__(self, entity_types, relation_types, examples, model_name="llama3-70b-8192", temperature=0):
        system_prompt = PromptTemplate(
            template="""You are a top-tier algorithm designed for extracting information in structured formats to build a knowledge graph.
            Your task is to identify the entities and relations requested with the user prompt, from a given text.
            You must generate the output in a JSON containing a list with JSON objects having the following keys: "head", "head_type", "relation", "tail", and "tail_type".
            The "head" key must contain the text of the extracted entity with one of the types from the provided list in the user prompt.
            The "head_type" key must contain the type of the extracted head entity which must be one of the types from {entity_types}.
            The "relation" key must contain the type of relation between the "head" and the "tail" which must be one of the relations from {relation_types}.
            The "tail" key must represent the text of an extracted entity which is the tail of the relation, and the "tail_type" key must contain the type of the tail entity from {entity_types}.
            Attempt to extract as many entities and relations as you can.

            IMPORTANT NOTES:
            - Don't add any explanation and text.
            """,
            input_variables=["entity_types", "relation_types"],
        )
        system_message_prompt = SystemMessagePromptTemplate(prompt=system_prompt)

        parser = JsonOutputParser(pydantic_object=ExtractedInfo)

        human_prompt = PromptTemplate(
            template="""Based on the following example, extract entities and relations from the provided text.\n\n

            Use the following entity types, don't use other entity that is not defined below:
            # ENTITY TYPES:
            {entity_types}

            Use the following relation types, don't use other relation that is not defined below:
            # RELATION TYPES:
            {relation_types}

            Below are a number of examples of text and their extracted entities and relationshhips.
            {examples}

            For the following text, generate extract entitites and relations as in the provided example.\n{format_instructions}\nText: {text}""",
            input_variables=["entity_types", "relation_types", "examples", "text"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        human_message_prompt = HumanMessagePromptTemplate(prompt=human_prompt)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        groq_api = os.environ.get("groq_api_key")  # Ensure you have this set
        if not groq_api:
            raise ValueError("groq_api_key environment variable not set.")
        self.model = ChatGroq(temperature=temperature, model_name=model_name, api_key=groq_api)
        # self.chain = LLMChain(llm=self.model, prompt=chat_prompt)
        self.chain = chat_prompt | self.model

    def extract_relations_from_sentence(self, sentence, entity_types, relation_types, examples):
        response = self.chain.invoke({
            'entity_types':entity_types, 
            'relation_types':relation_types, 
            'examples':examples, 
            'text':sentence
        })

        content = response.content
        try:
            return eval(content)
        except Exception as e:
            print("Error parsing content:", e)