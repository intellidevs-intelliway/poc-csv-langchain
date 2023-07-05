import streamlit as st
from st_pages import add_page_title
from sql_bot import Sql_Bot
from streamlit_chat import message
from dotenv import load_dotenv
import os
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

db_path = os.path.abspath('src\\db\\chinook.db')

st.markdown("### Como este é um bot de demonstração, ele já tem um banco de dados, mas os bancos de dados SQL mais populares podem ser utilizados com ele, como MS SQLServer, MySql, sqlite, Postgres, etc.")
st.markdown("#### Note que o único conhecimento e referências do bot estão na base de dados, então apelidos, gírias e palavras que fazem referência aos dados, mas que não foram passados, não serão compreendidos.")

uri = st.text_input(label="URI do banco de dados")
st.info("Deixe em branco para utilizar o banco de dados experimental default (chinook.db https://www.sqlitetutorial.net/sqlite-sample-database/)")

if uri:
    user_prompt = st.text_area(label="Pergunte ao banco de dados")

    if user_prompt:
        with st.spinner(text="Cada coisa doida nesse banco, calma aê..."):
            sql_bot = Sql_Bot()
            response = sql_bot.query_sql(user_input=user_prompt, db_url=db_path, db_uri=uri)
            if response == "Agent stopped due to iteration limit or time limit.":
                bot_response = "Hmmmmm... não entendi bem, pode tentar reformular a sua pergunta?"
                message(user_prompt, is_user=True)
                message(bot_response)
            else:
                message(user_prompt, is_user=True)
                message(response.strip())
else:
    # st.warning("Por favor, informe a URI do seu banco de dados para continuar.", icon="⚠️")
    user_prompt = st.text_area(label="Pergunte ao banco de dados")

    if user_prompt:
        with st.spinner(text="Cada coisa doida nesse banco, calma aê..."):
            sql_bot = Sql_Bot()
            response = sql_bot.query_sql(user_input=user_prompt, db_url=db_path, db_uri=uri)
            if response == "Agent stopped due to iteration limit or time limit.":
                bot_response = "Hmmmmm... não entendi bem, pode tentar reformular a sua pergunta?"
                message(user_prompt, is_user=True)
                message(bot_response)
            else:
                message(user_prompt, is_user=True)
                message(response.strip())
