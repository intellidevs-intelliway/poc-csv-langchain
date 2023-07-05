from typing import Dict, Any
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.utilities import PythonREPL
import textwrap
from dotenv import load_dotenv
load_dotenv()
import os

class MongoChain:
    def __init__(self, connection_string: str, database: str, collection: str):
        self.connection_string = str(connection_string).strip()
        self.database = str(database).strip()
        self.collection = str(collection).strip()
    
    def detect_intent(self, query: str = "") -> str:
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k", verbose=True)
        
        python_repl = PythonREPL()
        
        cmd = f"""
import subprocess
import sys

try:
    import pymongo
    from pymongo import MongoClient
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymongo"])

try:
    client = MongoClient('{self.connection_string}')
    db = client['{self.database}']
    collection = db['{self.collection}']
    
    result = collection.find().limit(1)
    
    for document in result:
        print(document)
except Exception as e:
    print(str(e))
"""

        sample = python_repl.run(cmd)
        
        template = """Given the following documentation and user input, extract from the input which method for collection is the most suitable one to do what the user wants and, if the user informs something that can be used as a query filter (id, name, etc), construct the correct command with the filter.
        Insert Documents:
        insert_one: Inserts a single document into a collection.
        
        document = {{"name": "John Doe", "age": 25}}
        collection.insert_one(document)
        insert_many: Inserts multiple documents into a collection.
        documents = [
            {{"name": "John Doe", "age": 25}},
            {{"name": "Jane Smith", "age": 30}}
        ]
        collection.insert_many(documents)
        
        Find Documents:
        find_one: Retrieves a single document from a collection.
        Full command: collection.find_one(query, projection)
        document = collection.find_one({{"name": "John Doe"}})
        find: Retrieves multiple documents from a collection.
        documents = collection.find({{"age": {{"$gt": 20}}}})
        for document in documents:
            print(document)
            
        Update Documents:
        update_one: Updates a single document in a collection.
        filter = {{"name": "John Doe"}}
        update = {{"$set": {{"age": 30}}}}
        collection.update_one(filter, update)
        update_many: Updates multiple documents in a collection.
        filter = {{"age": {{"$lt": 30}}}}
        update = {{"$inc": {{"age": 1}}}}
        collection.update_many(filter, update)
        
        Delete Documents:
        delete_one: Deletes a single document from a collection.
        filter = {{"name": "John Doe"}}
        collection.delete_one(filter)
        delete_many: Deletes multiple documents from a collection.
        filter = {{"age": {{"$gte": 40}}}}
        collection.delete_many(filter)
        
        Aggregation:
        aggregate: Performs aggregation operations on a collection.
        pipeline = [
            {{"$match": {{"age": {{"$gt": 25}}}}}},
            {{"$group": {{"_id": "$city", "count": {{"$sum": 1}}}}}}
        ]
        results = collection.aggregate(pipeline)
        for result in results:
            print(result)
        
        If the user refers to 'id', understand it as '_id'.
        
        Take this collection object as sample as a means of understanding how this collection is structured: {sample}
        
        This is the user's query: {input}
        
        Feel free to return the command that best fits the user's description, but you must only return the command.
        
        pymongo command: """
        
        prompt = PromptTemplate(template=template, input_variables=['input', 'sample'])
        
        chain = LLMChain(llm=llm, prompt=prompt)
        
        res = chain.run(input=query, sample=sample)
        
        # TODO -> get intent and run it through the next function (run_query), which will return the query results
        # run query results through llm with the user's initial prompt and return to the view
        
        # return res
        query_res = self.run_query(command=res.strip(), input=query)
        
        return query_res
    
    def evaluate_response(self, evaluate: str = "", user_query: str = ""):
        llm = ChatOpenAI(temperature=0.5, model='gpt-3.5-turbo-16k')
        
        template = """Take the following user input: {input}
        Now, interpret the following result from a mongodb query: {query}
        
        Interpret what the user wants to know from this query result. If what the user wants to know is not in the query result, apologize and inform the user of this in a polite way.
        If what the user wants to know is in the query reult, inform the user of this in a charismatic and informative way. Display whatever information from the query was passed down to you.
        
        Your response:"""
        
        prompt = PromptTemplate(template=template, input_variables=['input', 'query'])
        
        chain = LLMChain(llm=llm, verbose=True, prompt=prompt)
        
        res = chain.run(input=user_query, query=evaluate)
        
        return res
        
    # def run_query(self, intention: str = 'find', connection_string: str = "", query = {}) -> str:
    def run_query(self, command: str = "", input: str = "") -> str:
        python_repl = PythonREPL()
        
        print(f"Command: {command}")
        
        cmd = f"""
import subprocess
import sys

try:
    import pymongo
    from pymongo import MongoClient
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymongo"])

try:
    client = MongoClient('{self.connection_string}')
    db = client['{self.database}']
    collection = db['{self.collection}']
"""
        if "find" in command:
            cmd = cmd + f"""    results = {command}
    if isinstance(results, pymongo.cursor.Cursor):
        results = list(results)
    
    if isinstance(results, list):
        data = []
        for res in results:
            data.append(res)
        print(data)
    else:
        print(results)
        
    client.close()
except Exception as e:
    print(str(e))"""
            
        elif "update" in command:
            cmd = cmd + f"""    {command}
    print('Update successful!')
    client.close()
except Exception as e:
    print(str(e))"""
    
        elif "delete" in command:
            cmd = cmd + f"""    {command}
    print('Database entry deleted successfully!')
    client.close()
except Exception as e:
    print(str(e))"""
        
        elif "insert" in command:
            cmd = cmd + f"""    {command}
    print('Database entry created successfully!')
    client.close()
except Exception as e:
    print(str(e))"""
        
        print(cmd)

        res = python_repl.run(cmd)
        
        print("Python result: ", res)
        
        temp = self.evaluate_response(evaluate=res, user_query=input)
        
        return temp
    
        # return res 
        
# if __name__ == '__main__':
#     chain = MongoChain(connection_string=os.getenv('MONGO_CONNECTION_STRING'), database='dummy', collection='dummy-collection')
#     res = chain.detect_intent(query="show everything in this database.")
#     # res = MongoChain.run_query(connection_string=os.getenv("MONGO_CONNECTION_STRING"), command="collection.find_one({'name': 'Smartphone 1'})", input="")
#     print(res)





















# import sys
# from io import StringIO
# from typing import Dict, Optional

# from pydantic import BaseModel, Field


# class PythonREPL(BaseModel):
#     """Simulates a standalone Python REPL."""

#     globals: Optional[Dict] = Field(default_factory=dict, alias="_globals")
#     locals: Optional[Dict] = Field(default_factory=dict, alias="_locals")

#     def run(self, command: str) -> str:
#         """Run command with own globals/locals and returns anything printed."""
#         old_stdout = sys.stdout
#         sys.stdout = mystdout = StringIO()
#         try:
#             exec(command, self.globals, self.locals)
#             sys.stdout = old_stdout
#             output = mystdout.getvalue()
#         except Exception as e:
#             sys.stdout = old_stdout
#             output = repr(e)
#         return output
