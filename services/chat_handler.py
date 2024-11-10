import streamlit as st
from services.service_interface import ServiceInterface

def start_chat(evaluator_dict: dict, user_name: str, service: ServiceInterface):
    """
    Inicia um chat com o usuário e permite troca de mensagens até clicar em "Avaliação".
    
    Args:
        user_name (str): Nome do usuário em atendimento.
        evaluator_dict (dict): Dados do avaliador.
        service (ServiceInterface): Serviço que fornece a interface para o chat e outras interações.
    """

    st.subheader(f"Conversando com {user_name}")
    
    # Inicializa o histórico do chat no estado da sessão, se ainda não existir
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = f"Início do chat com {user_name}.\n"

    # Área de exibição do histórico de chat
    st.text_area("Histórico do Chat", value=st.session_state.chat_history, height=300, disabled=True)

    # Inicializa a nova mensagem no estado da sessão, se ainda não existir
    if "new_message" not in st.session_state:
        st.session_state.new_message = ""

    # Campo de entrada para a nova mensagem
    new_message = st.text_input("Digite sua mensagem:", key="new_message_input", value=st.session_state.new_message)

    # Botão de envio da mensagem fora do formulário
    if st.button("Enviar"):
        if new_message:
            # Atualiza o histórico com a nova mensagem concatenada ao chat anterior
            full_message = st.session_state.chat_history + "\n" + f"Avaliador: {new_message}"
            response = service.chat_with_user(full_message)  # Envia para o serviço

            # Atualiza o histórico do chat com a resposta recebida
            st.session_state.chat_history = full_message + "\n" + f"{user_name}: {response}"

            # Limpa o campo de entrada da nova mensagem
            st.session_state.new_message = ""  # Reseta o valor para o próximo envio
            st.experimental_rerun()

    # Botão de "Avaliação" para finalizar o chat
    if st.button("Avaliação"):
        if st.session_state.chat_history:
            # Envia o histórico completo para os serviços de avaliação
            service.finalize_evaluation(st.session_state.chat_history)
            st.success("Conversa enviada para avaliação.")
            st.write("Obrigado por utilizar o PsiAI")
            
            # Limpa o histórico de chat após a avaliação
            del st.session_state.chat_history
            st.experimental_set_query_params(page="home")
            st.experimental_rerun()
