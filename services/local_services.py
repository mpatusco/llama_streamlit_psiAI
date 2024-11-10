from services.service_interface import ServiceInterface
from langchain_groq import ChatGroq
from .utils.experience_eval import ExperienceEval 
import json
import pandas as pd

SYSTEM_PROMPT = """You are a helpful chatbot that simulates an user with a mental disorder to help a psychologist diagnose your mental disorder. Your conversation must be in a way to aid the psychologist learn your mental disorder based in your responses, but not writing what is it

### EMULATED USER PROFILE
Your profile as a user is the following:
- Name: {username}
- Age: {age}
- Profession: {profession}
- Mental Disorder: {mental_disorder}
- Location: {location}
- Life Issues: {life_issues}
- Persona: {persona}
- Backstory: {backstory}

### RESPONSE GUIDANCE
Your responses must be in english, as the psychologist question and interaction will also be in this language.
Also, do not format your response as a list and in the beginning of conversation say what is your name and be as concise as possible.
"""

def get_llm():
    llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=1,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )
    return llm

class LocalService(ServiceInterface):
    def send_profile(self, profile_data):
        return {"status": "success"}

    def get_profile_info(self):
        return {"nome": "Teste Usuário"}

    def chat_with_user(self, messages, profile):
        system_prompt = SYSTEM_PROMPT.format(**profile)
        messages = ["system", system_prompt] + messages
        llm = get_llm()
        llm_response = llm.invoke(messages).content
        return llm_response

    def finalize_evaluation(self, chat_history, profile, psy_diagnosis):
        df_disorder = pd.read_csv("services/dataset_transtornos_mentais_v4.csv")
        disorder = df_disorder[df_disorder["label"] == profile["mental_disorder"]]
        conversation_example = ""
        for message in chat_history:
            if message[0] == 'ai':
                conversation_example += "Patient: "+ message[1] + "\n\n"
            else:
                conversation_example += "Psychologist: "+ message[1] + "\n\n"
        
        while True:
            try:
                evaluator = ExperienceEval()

                result = evaluator.invoke(user_profile=profile,
                                        disorder=disorder["label"].values[0],
                                        description=disorder["description"].values[0],
                                        symptom=disorder["symptom"].values[0],
                                        diagnosis=disorder["diagnosis"].values[0],
                                        treatment=disorder["treatment"].values[0],
                                        chat_history=conversation_example,
                                        psy_diagnosis=psy_diagnosis)
                return result
            except:
                print('Trying again in 1 second')
                import time
                time.sleep(1)
    
    def get_users(self):
        return [{'username': 'Felipe',
                'age': '32',
                'profession': 'Data Scientist',
                'mental_disorder': 'Autism Spectrum Disorder',
                'location': 'São Paulo, Brazil',
                'life_issues': 'dont like the workplace because people dont understand him',
                'persona': 'an outgoing person that likes to talk. However, for some reason likes to talk in a formal matter',
                'backstory': 'likes to play guitar'},
                {'username': 'Ana',
                'age': '20',
                'profession': 'Graphic Designer',
                'mental_disorder': 'Persistent Depressive Disorder',
                'location': 'São Paulo, Brasil',
                'life_issues': 'feels alone because lives in a house by herself',
                'persona': 'A reserved person that dont like to talk to much with other people',
                'backstory': 'parents lives in the countryside'}
                ]