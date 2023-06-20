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

    def run_agent(self, prompt: str, df: pd.DataFrame) -> str:
        # agent = create_csv_agent(OpenAI(temperature=0), files, verbose=True)
        agent_csv = create_pandas_dataframe_agent(ChatOpenAI(temperature=0.7, model='gpt-3.5-turbo-16k'), df=df, verbose=True)
        full_prompt = f"""
        You are a curator bot who speaks Brazilian Portuguese and who will receive some knowledge and will retrieve all the information the user asks for in the most detailed way possible.
        No one-word responses, always form and return full sentences for your final answers.
        Your responses must be returned in Brazilian Protuguese.
        Please provide the most complete answer possible to the following prompt:
        {prompt}
        """
        result = agent_csv.run(full_prompt)
        return result

    def run_prompt(self, prompt):
        df: pd.DataFrame
        if self.files:
            for file in self.files:
                path = f"files/{file}"
                separators = r";|,"
                df = pd.read_csv(path, on_bad_lines='skip', sep=separators, encoding='latin-1', engine='python')
                self.file_paths.append(path)
            # print(df)
            
            try:
                response = str(self.run_agent(prompt=prompt, df=df))
                # return self.translate(response, 'pt-br')
                return response
            except:
                return "Houve um erro ao ler o arquivo ou ao interpretar a sua pergunta. Verifique a formatação ou reformule sua pergunta."

        else:
            return 'Não achei nenhum arquivo nesse diretório *sigh*'

# if __name__ == '__main__':
#     run("Which comedy movies has Antonio Banderas been in?")