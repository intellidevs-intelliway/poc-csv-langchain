from bot import Bot
from streamlit_chat import message
import streamlit_authenticator as stauth

import streamlit as st

import os
from dotenv import load_dotenv
load_dotenv()

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

st.set_page_config(page_title="Chatbot Proof Of Concept", page_icon=":robot", layout="centered")

hashed = stauth.Hasher(["abc123"]).generate()

credentials = {
    "usernames": {
        "admin": {
            "email": "admin@email.com",
            "name": "Admin",
            "password": hashed[0]
        }
    }
}

cookie = {
    "expiry_days": 30,
    "key": "bot_chat_window",
    "name": "main_cookie"
}

preauthorized = {
    "emails": [
        "admin@email.com"
    ]
}

authenticator = stauth.Authenticate(credentials=credentials, cookie_name=cookie["name"], key=cookie["key"], cookie_expiry_days=cookie["expiry_days"], preauthorized=preauthorized)
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Combinação usuário/senha inválida.")
    
if authentication_status == None:
    st.warning("Informe o usuário e a senha.")
    
if authentication_status == True:
    st.markdown("# Proof Of Content Chatbot")
    st.markdown(f"### Bom te ver, :orange[{name}]!")
    st.divider()
    authenticator.logout(button_name="Logout", location="main")
    
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
    
