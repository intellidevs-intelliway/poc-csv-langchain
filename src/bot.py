import shutil
from langchain.agents import create_csv_agent, create_pandas_dataframe_agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import pandas as pd
import csv
import os
from dotenv import load_dotenv
load_dotenv()

class Bot:
    def __init__(self) -> None:
        self.file_paths = []
        self.files = os.listdir('files')
        
    def translate(self, prompt: str, to: str, _from: str=None) -> str:
        llm = OpenAI(temperature=0)
        full_query = f"""You are a translator bot who must simply translate the given input to {to}.
        Do not translate important keywords that are relevant to the context, such as movie names, song names, band names, people and places.
        Never translate proper nouns.
        Now, given the aforementioned rules, translate this:
        {prompt}.
        
        Your translation: """
        
        response = str(llm(full_query))
        return response

    def run_agent(self, prompt: str, df: pd.DataFrame, example_rows: pd.DataFrame) -> str:
        # agent = create_csv_agent(OpenAI(temperature=0), files, verbose=True)
        agent_csv = create_pandas_dataframe_agent(OpenAI(temperature=0), df=df, verbose=True)
        full_prompt = f"""
        You are a curator bot who speaks Brazilian Portuguese and who will receive some knowledge and will retrieve all the information the user asks for in the most detailed way possible.
        No one-word responses, always form and return full sentences for your final answers.
        Your responses must be returned in Brazilian Protuguese.
        Given the example rows provided, study their structure in order to perfect your queries on the dataframe:
        {example_rows}
        Now, interpret what the user wants with the following prompt and extract it from the dataframe: {prompt}
        Now, return your response in the most complete way possible:"""
        
        result = agent_csv.run(full_prompt)
        return result

    def run_prompt(self, prompt):
        df: pd.DataFrame
        if self.files:
            for file in self.files:
                path = f"files/{file}"
                delimiter = ";"
                df = pd.read_csv(path, on_bad_lines='skip', delimiter=delimiter, encoding='utf-8')
                self.file_paths.append(path)
            example_rows = df.head(5)
            response = self.run_agent(prompt=prompt, df=df, example_rows=example_rows)
            if response == "Agent stopped due to iteration limit or time limit.":
                for file in self.files:
                    path = f"files/{file}"
                    df = pd.read_csv(path, on_bad_lines='skip', encoding='utf-8')
                    self.file_paths.append(path)
                example_rows = df.head(5)
                response = self.run_agent(prompt=prompt, df=df, example_rows=example_rows)
                                
            return response
        else:
            return 'Não achei nenhum arquivo nesse diretório *sigh*'
