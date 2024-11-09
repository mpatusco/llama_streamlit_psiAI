import streamlit as st
from services import chat_handler
from config import get_service
from validator import FormValidator

# Configurações do serviço AWS ou fake
service = get_service()

# Validadores para cada formulário
profile_validator = FormValidator(["nome", "idade", "persona", "diagnostico", "profissao", "problemas", "local"])
evaluator_validator = FormValidator(["nome", "registro"])

def main():
    # Configuração do título da aplicação
    st.title("PsiAI")

    # Captura o parâmetro de URL 'page' para decidir qual página exibir
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["home"])[0]
    if page == "home":
        home_page()
    elif page == "add_profile":
        new_profile_form()
    elif page == "evaluator":
        evaluator_form()

def home_page():
    option = None
    next_page = False
    st.subheader("Bem-vindo ao PsiAI")
    option = st.selectbox("Escolha uma ação", ["Adicionar Perfil", "Interagir como Avaliador"])
    next_page = st.button("Avançar")
    if next_page and option == "Adicionar Perfil":
        st.experimental_set_query_params(page="add_profile")
        st.experimental_rerun()
    elif next_page and option == "Interagir como Avaliador":
        st.experimental_set_query_params(page="evaluator")
        st.experimental_rerun()

def new_profile_form():
    # Inicializa os valores padrão dos campos no estado da sessão
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
        nome = st.text_input("Nome", value=st.session_state.form_data["nome"])
        idade = st.number_input("Idade", min_value=0, value=st.session_state.form_data["idade"])
        persona = st.text_area("Persona", value=st.session_state.form_data["persona"])
        diagnostico = st.text_area("Diagnóstico", value=st.session_state.form_data["diagnostico"])
        profissao = st.text_input("Profissão", value=st.session_state.form_data["profissao"])
        problemas = st.text_area("Problemas de vida", value=st.session_state.form_data["problemas"])
        local = st.text_input("Local", value=st.session_state.form_data["local"])

        enviar = st.form_submit_button("Enviar")
        novo_perfil = st.form_submit_button("Criar novo perfil")

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
                service.send_profile(perfil_data)
                st.success("Perfil enviado com sucesso!")

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
            st.experimental_rerun()

    if st.button("Voltar para a página inicial"):
        st.experimental_set_query_params(page="home")
        st.experimental_rerun()

def evaluator_form():
    st.subheader("Avaliador")
    nome = st.text_input("Nome do Avaliador")
    registro = st.text_input("Número de Registro")
    iniciar = st.button("Iniciar Atendimento")

    if iniciar:
        evaluator_data = {
            "nome": nome,
            "registro": registro
        }

        # Validação usando o FormValidator
        is_valid, error_message = evaluator_validator.validate(evaluator_data)
        if not is_valid:
            st.error(error_message)
        else:
            user_data = service.get_profile_info()
            st.write(f"Atendimento iniciado com a pessoa {user_data['nome']}")
            chat_handler.start_chat(evaluator_data, user_data["nome"], service)

    # Separando o botão "Voltar para a página inicial" para evitar conflitos
    if st.button("Voltar para a página inicial"):
        st.experimental_set_query_params(page="home")
        st.experimental_rerun()

if __name__ == "__main__":
    main()
