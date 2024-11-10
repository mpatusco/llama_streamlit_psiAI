from dataclasses import dataclass
from typing import Literal
import streamlit as st

import getpass
import os

from langchain_groq import ChatGroq
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict
import streamlit.components.v1 as components
from config import get_service
from services import chat_handler
from validator import FormValidator

if 'service' not in st.session_state:
    st.session_state.service = get_service()

# Validadores para cada formulário
profile_validator = FormValidator(["nome", "idade", "persona", "diagnostico", "profissao", "problemas", "local"])
evaluator_validator = FormValidator(["nome", "registro"])


def load_css():
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = {}
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0

def on_click_callback():
    human_prompt = st.session_state.human_prompt
    messages = st.session_state.history + [("human", human_prompt)]
    llm_response = st.session_state.service.chat_with_user(messages)  # Envia para o serviço
    st.session_state.history.append(
        ["human", human_prompt] 
    )
    st.session_state.history.append(
        ["ai", llm_response]
    )

load_css()
initialize_session_state()

st.title("Simulate a patient 🤖")

@st.dialog("Create a new profile")
def create_profile():
    if "form_data" not in st.session_state:
        st.session_state.form_data = {
            "nome": "",
            "idade": 0,
            "persona": "",
            "diagnostico": "",
            "profissao": "",
            "problemas": "",
            "local": ""
        }

    st.subheader("Novo Perfil")
    with st.form(key="new_profile_form"):
        nome = st.text_input("Name", value=st.session_state.form_data["nome"])
        idade = st.number_input("Age", min_value=0, value=st.session_state.form_data["idade"])
        persona = st.text_area("Persona", value=st.session_state.form_data["persona"])
        diagnostico = st.text_area("Diagnose", value=st.session_state.form_data["diagnostico"])
        profissao = st.text_input("Profession", value=st.session_state.form_data["profissao"])
        problemas = st.text_area("Life Problems", value=st.session_state.form_data["problemas"])
        local = st.text_input("Local", value=st.session_state.form_data["local"])

        enviar = st.form_submit_button("Save changes")
        novo_perfil = st.form_submit_button("End Submission")

        if enviar:
            perfil_data = {
                "nome": nome,
                "idade": idade,
                "persona": persona,
                "diagnostico": diagnostico,
                "profissao": profissao,
                "problemas": problemas,
                "local": local
            }

            # Validação usando o FormValidator
            is_valid, error_message = profile_validator.validate(perfil_data)
            if not is_valid:
                st.error(error_message)
            else:
                st.session_state.service.send_profile(perfil_data)
                st.success("Profile saved with sucess!")

        if novo_perfil:
            st.session_state.form_data = {
                "nome": "",
                "idade": 0,
                "persona": "",
                "diagnostico": "",
                "profissao": "",
                "problemas": "",
                "local": ""
            }
            st.rerun()


tab1, tab2= st.tabs(["New Profile", "Chat"])

with tab1:
    if st.button("Create a new profile"):
        create_profile()

with tab2:
    users = st.session_state.service.get_users()
    names = [x['username'] for x in users]
    selection = st.pills(
        "Users",
        options=names,
        selection_mode="single",
    )
    userdata = {x['username']: x for x in users}
    if selection:
        chat_handler.start_chat(userdata[selection], selection)

