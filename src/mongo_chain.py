import streamlit as st
from st_pages import add_page_title
from mongo_chain import MongoChain
from streamlit_chat import message
from bs4 import BeautifulSoup
import os
import requests
from dotenv import load_dotenv
load_dotenv()

add_page_title(layout="centered")

try:
    files_list = os.listdir('files')
    if files_list:
        for file in files_list:
            file_path = os.path.join('files', file)
            if os.path.isfile(file_path):
                os.remove(file_path)
except FileNotFoundError:
    print('caught')
    os.mkdir('files')

st.markdown("### Informe os dados nos campos abaixo e converse com seus bancos de dados do MongoDB!")

connection_string = st.text_input(label="String de conexão do seu banco")
# st.info(body="Para saber mais sobre como ativar e utilizar essa funcioalidade, acesse https://www.mongodb.com/docs/atlas/api/")

# datasource = st.text_input(label="Datasource/Nome do Cluster")

database = st.text_input(label="Database")

collection = st.text_input(label="Collection")

if connection_string and database and collection:
    prompt = st.text_area(label="Converse com seu banco de dados")
    if prompt:
        with st.spinner("Executando..."):
            mongo = MongoChain(connection_string=connection_string, database=database, collection=collection)
            res = mongo.detect_intent(prompt)
            
            if res:
                message(prompt, is_user=True)
                message(res.strip())

else:
    st.error("Informe todos os campos.")
