import streamlit as st
from st_pages import add_page_title
from api_bot import Api_Bot
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

st.markdown("### Como este é um bot de demonstração, ele já tem uma API pré configurada. No entanto, para utilizar qualquer API, basta informar a documentação da API para que o bot aprenda a estrutura das requisições.")
st.markdown("#### Note que o único conhecimento e referências do bot estão na documentação da API que foi passada, então o bot não consegue realizar nada fora desta.")

link = st.text_input(label="Link para a documentação da API")

if link:
    try:
        with st.spinner(text="Adoro clicar em links aleatórios *risada sarcástica*"):
            page_contents = requests.get(link)
            soup = BeautifulSoup(page_contents.content, 'html.parser')
            body_tag = soup.find('body')
            api_docs = body_tag.get_text()
            
        user_prompt = st.text_area(label="Pergunte à API")

        if user_prompt:
            with st.spinner(text="Olha lá hein, tá me mandando pra onde?"):
                api_bot = Api_Bot()
                response = api_bot.get_from_api(input=user_prompt, api_docs=api_docs)
                if response == "Agent stopped due to iteration limit or time limit.":
                    bot_response = "Hmmmmm... não entendi bem, pode tentar reformular a sua pergunta?"
                    message(user_prompt, is_user=True)
                    message(bot_response)
                else:
                    message(user_prompt, is_user=True)
                    message(response)
        
    except:
        st.error("O link informado retornou um erro. Por favor, tente outro link.")
