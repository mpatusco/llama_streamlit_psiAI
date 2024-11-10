import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go


def on_click_callback():
    human_prompt = st.session_state.human_prompt
    messages = st.session_state.history[st.session_state.current_username] + [("human", human_prompt)]
    llm_response = st.session_state.service.chat_with_user(messages, st.session_state.current_user_data)  # Envia para o serviço
    st.session_state.history[st.session_state.current_username].append(
        ("human", human_prompt)
    )
    st.session_state.history[st.session_state.current_username].append(
        ("ai", llm_response)
    )

def start_chat(userdata: dict, user_name: str):
    """
    Inicia um chat com o usuário e permite troca de mensagens até clicar em "Avaliação".
    
    Args:
        user_name (str): Nome do usuário em atendimento.
        evaluator_dict (dict): Dados do avaliador.
        service (ServiceInterface): Serviço que fornece a interface para o chat e outras interações.
    """

    st.subheader(f"Talking to {user_name}")
    chat_placeholder = st.container()
    prompt_placeholder = st.form("chat-form")
    st.session_state.current_username = user_name
    st.session_state.current_user_data = userdata
    if user_name not in st.session_state.history:
        st.session_state.history[user_name] = []
    with chat_placeholder:
        for chat in st.session_state.history[user_name]:
            div = f"""
    <div class="chat-row 
        {'' if chat[0] == 'ai' else 'row-reverse'}">
        <img class="chat-icon" src="app/static/{
            'ai_icon.png' if chat[0] == 'ai' 
                        else 'user_icon.png'}"
            width=32 height=32>
        <div class="chat-bubble
        {'ai-bubble' if chat[0] == 'ai' else 'human-bubble'}">
            &#8203;{chat[1]}
        </div>
    </div>
            """
            st.markdown(div, unsafe_allow_html=True)
        
        for _ in range(3):
            st.markdown("")

    with prompt_placeholder:
        st.markdown("**Chat**")
        cols = st.columns((6, 1))
        cols[0].text_input(
            "Chat",
            value="",
            label_visibility="collapsed",
            key="human_prompt",
        )
        cols[1].form_submit_button(
            "Submit", 
            type="primary", 
            on_click=on_click_callback, 
        )

    components.html("""
    <script>
    const streamlitDoc = window.parent.document;

    const buttons = Array.from(
        streamlitDoc.querySelectorAll('.stButton > button')
    );
    const submitButton = buttons.find(
        el => el.innerText === 'Submit'
    );

    streamlitDoc.addEventListener('keydown', function(e) {
        switch (e.key) {
            case 'Enter':
                submitButton.click();
                break;
        }
    });
    </script>
    """, 
        height=0,
        width=0,
    )
    # Botão de "Avaliação" para finalizar o chat
    if st.button("Evaluation"):
        
        if st.session_state.history[user_name]:
            evaluate()

@st.dialog("Diagnose Evaluation",width = 'large')
def evaluate():
    diagnose =  st.text_area(
        "Write your diagnose"
    )
    if st.button('Get Diagnose'):
        with st.spinner('Loading the psycologist evaluation'):
            result = st.session_state.service.finalize_evaluation(st.session_state.history, st.session_state.current_user_data, diagnose)
        categories = [
            'Symptoms Exploration',
            'Active Listening and Empathy',
            'Anamnesis Detailing',
            'Symptoms Identification',
            'Clinical Reasoning',
            'Diagnosis Accuracy',
            'Service Quality'
        ]

        scores = [
            result['symptoms_exploration'],
            result['active_listening_empathy_response'],
            result['anamnesis_detailing_response'],
            result['symptoms_identification_response'],
            result['clinical_reasoning_response'],
            result['diagnosis_accuracy_response'],
            result['service_quality_response']
        ]

        scores.append(scores[0])
        categories.append(categories[0])

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='Evaluation',
            marker=dict(color='blue')
        ))

        fig.update_layout(
            title="Response Evaluation",
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )
            ),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader('Exploration of symptons')
        st.write('Grade: '+ str(result['symptoms_exploration']))
        st.write('Explanation: '+ str(result['justification_symptoms_exploration']))

        st.subheader('Active listening empathy')
        st.write('Grade: '+ str(result['active_listening_empathy_response']))
        st.write('Explanation: '+ str(result['justification_active_listening_empathy']))

        st.subheader('Anamnesis detailing')
        st.write('Grade: '+ str(result['anamnesis_detailing_response']))
        st.write('Explanation: '+ str(result['justification_anamnesis_detailing']))

        st.subheader('Symptoms Identification')
        st.write('Grade: '+ str(result['symptoms_identification_response']))
        st.write('Explanation: '+ str(result['justification_symptoms_identification']))

        st.subheader('Clinical reasoning')
        st.write('Grade: '+ str(result['clinical_reasoning_response']))
        st.write('Explanation: '+ str(result['justification_clinical_reasoning']))

        st.subheader('Diagnosis Accuracy')
        st.write('Grade: '+ str(result['diagnosis_accuracy_response']))
        st.write('Explanation: '+ str(result['justification_client_escalation']))

        st.subheader('Service Quality')
        st.write('Grade: '+ str(result['service_quality_response']))
        st.write('Explanation: '+ str(result['justification_service_quality']))


    if st.button('End Evaluation'):
        st.success("Thanks for using our system.")
