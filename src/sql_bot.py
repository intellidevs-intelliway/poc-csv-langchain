from langchain import OpenAI, PromptTemplate, SQLDatabase, SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import SQLDatabaseSequentialChain
from bot import Bot

class Sql_Bot:
    def __init__(self):
        pass
    
    def query_sql(self, user_input: str, db_url: str, db_uri: str):
        template = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer in the same language as the one used in the input.
        Use the following format:

        Question: "Question here"
        SQLQuery: "SQL Query to run"
        SQLResult: "Result of the SQLQuery"
        Answer: "Final answer here"

        Only use the following tables:

        {table_info}

        Question: {input}"""

        prompt = PromptTemplate(
            input_variables=["dialect", "table_info", "input"], template=template
        )

        try:    
            if db_uri != '':
                print(db_uri)
                db = SQLDatabase.from_uri(
                database_uri=db_uri
            )
            else:
                print(db_url)
                db = SQLDatabase.from_uri(
                database_uri=f"sqlite:///{db_url}"
            )
            
            llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo-16k", verbose=True)
            
            try:
                print("Attempting query...")
                sql_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, prompt=prompt, verbose=True)
                result = sql_chain.run(user_input)
                bot = Bot()
                return bot.translate(prompt=result, to='pt-br')
            
            except:
                print("Attempting sequential query...")
                sql_chain = SQLDatabaseSequentialChain.from_llm(llm=llm, database=db, verbose=True)
                result = sql_chain.run(user_input)
                bot = Bot()
                return bot.translate(prompt=result, to='pt-br')
            
        except Exception as e:
            print(e)
            return 'Não consegui conectar ao banco de dados... verifique sua URI.'
