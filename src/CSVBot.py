import streamlit as st
from bot import Bot
from streamlit_chat import message
import os

from st_pages import add_page_title

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

file = st.file_uploader(label="Importe um arquivo .csv para começar a conversa.", type='csv', accept_multiple_files=False)
    
if file:
    with st.spinner("Lendo o arquivo... já preparou suas perguntas? ;)"):
        file_name = str(file.name)
        file_path = os.path.join('files', file_name)
        with open(file_path, "wb") as f:
            f.write(file.getvalue())
    st.success("Terminei de ler! Pergunte o que quiser sobre o arquivo.")
    
    user_prompt = st.text_area(label="Você diz: ")
    
    # ====================== Handling chat memory... ======================
    # if "user_prompt_history" not in st.session_state:
    #     st.session_state["user_prompt_history"] = []
    # if "chat_anwers_history" not in st.session_state:
    #     st.session_state["chat_anwers_history"] = []
        
    #     if "chat_history" not in st.session_state:
    #         st.session_state["chat_history"] = []
    # ====================== Handling chat memory... ======================
    
    if user_prompt:
        with st.spinner("Pesquisando sobre física quântica... calma, qual foi a sua pergunta?"):
            bot = Bot()
            response = bot.run_prompt(prompt=user_prompt)
            if response == "Agent stopped due to iteration limit or time limit.":
                bot_response = "Hmmmmm... não entendi bem, pode tentar reformular a sua pergunta?"
                message(user_prompt, is_user=True)
                message(bot_response)
            else:
                message(user_prompt, is_user=True)
                message(response)
