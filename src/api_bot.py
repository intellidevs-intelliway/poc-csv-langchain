from langchain import PromptTemplate
from langchain.chains import APIChain

from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

from langchain.chains.api import open_meteo_docs

class Api_Bot:
    def get_from_api(self, input, api_docs):
        
        llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo-16k')
        CUSTOM_API_URL_PROMPT_TEMPLATE = """You are given the below API Documentation:
        {api_docs}
        Using this documentation, generate the full API url to call for answering the user question.
        You should build the API url in order to get a response that is as short as possible, while still getting the necessary information to answer the question. Pay attention to deliberately exclude any unnecessary pieces of data in the API call.

        Understand tomorrow as today + one day.
        Example: today = June 15 2023.
        Tomrrow: today + 1 day = June 15 2023 + 1 day = June 16 2023

        Understand yesterday as today - one day.
        Example: today = June 15 2023.
        Tomrrow: today - 1 day = June 15 2023 - 1 day = June 14 2023

        Question:{question}
        API url:"""

        CUSTOM_API_URL_PROMPT = PromptTemplate(
            input_variables=[
                "api_docs",
                "question",
            ],
            template=CUSTOM_API_URL_PROMPT_TEMPLATE,
        )

        CUSTOM_API_RESPONSE_PROMPT_TEMPLATE = (
            CUSTOM_API_URL_PROMPT_TEMPLATE
            + """ {api_url}

        Here is the response from the API:

        {api_response}

        Summarize this response to answer the original question.
        Your response must be in the same language as the user input.

        Summary:"""
        )

        CUSTOM_API_RESPONSE_PROMPT = PromptTemplate(
            input_variables=["api_docs", "question", "api_url", "api_response"],
            template=CUSTOM_API_RESPONSE_PROMPT_TEMPLATE,
        )

        # API_DOCS = """""" -> FOR CUSTOM APIS
        chain = APIChain.from_llm_and_api_docs(llm=llm, api_docs=api_docs,
                                               api_url_prompt=CUSTOM_API_URL_PROMPT, api_response_prompt=CUSTOM_API_RESPONSE_PROMPT, verbose=True)
        
        result = chain.run(question=input)
        return result