import streamlit as st
import streamlit_authenticator as stauth
from st_pages import Page, Section, show_pages, add_page_title
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="IntelliBots",
    page_icon="🤖"
)

st.markdown("## Bem-vindo a nossa demonstração com diferentes tipos de bots!")

st.markdown("#### Nesta página, você poderá experimentar (de maneira limitada) as habilidades da IA generativa aplicadas a diferentes propósitos que visam facilitar a sua interação com seu ambiente de trabalho.")

st.markdown("#### Aqui está uma lista das habilidades disponíveis nesta página:")
st.markdown("- Bot leitor de arquivos no formato .csv")
st.markdown("- Bot leitor de bancos de dados relacionais (SQL)")
st.markdown("- Bot de APIs - faz chamadas de API e interpreta os resultados")
st.markdown("- Bot curador de bancos de dados não-relacionais (MongoDB) - :orange[Em desenvolvimento]")

st.markdown("#### Escolha um bot no menu ao lado e vamos começar!")

try:
    files_list = os.listdir('files')
    if files_list:
        for file in files_list:
            file_path = os.path.join('files', file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print('Files removed.')
except FileNotFoundError:
    print('caught')
    os.mkdir('files')

hashed = stauth.Hasher([os.getenv("USER_PASS"), os.getenv("INTELLIWAY_PASS")]).generate()

credentials = {
    "usernames": {
        "admin": {
            "email": "admin@email.com",
            "name": "Admin",
            "password": hashed[0]
        },
        "intelliway": {
            "email": "intelliway@intelliway.com.br",
            "name": "Intelliway",
            "password": hashed[1]
        }
    }
}

cookie = {
    "expiry_days": 1,
    "key": "bot_chat_window",
    "name": "main_cookie"
}


preauthorized = False
# preauthorized = {
#     "emails": [
#         "admin@email.com"
#     ]
# }

authenticator = stauth.Authenticate(credentials=credentials, cookie_name=cookie["name"], key=cookie["key"], cookie_expiry_days=cookie["expiry_days"], preauthorized=preauthorized)
name, authentication_status, username = authenticator.login("Login", "sidebar")

if authentication_status == False:
    st.sidebar.error("Combinação usuário/senha inválida.")
    
if authentication_status == None:
    st.sidebar.warning("Informe o usuário e a senha.")
    
if authentication_status == True:
    st.sidebar.markdown(f"### Bom te ver, :orange[{name}]!")
    authenticator.logout(button_name="Logout", location="sidebar")

    show_pages(
        [
            Page(path="src/main_page.py", name="Home", icon="🏠"),
            Page(path="src/CSVBot.py", name="Bot Leitor de CSV", icon="📄"),
            Page(path="src/SQLBot.py", name="Bot de SQL", icon="📊"),
            Page(path="src/APIBot.py", name="Bot de APIs", icon="🌐"),
            Page(path="src/MongoBot.py", name="MongoDBot", icon="🍃")
        ]
    )
