import os
from groq import Groq
from langchain.output_parsers.structured import ResponseSchema, StructuredOutputParser
from langchain_core.prompts.prompt import PromptTemplate

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

RESPONSE_SCHEMA = [
    ResponseSchema(name="symptoms_exploration", description="Was the psychologist thorough and careful in gathering information? Did they ask relevant questions and explore the main aspects of the condition? Answer from 1 to 5.", type="int"),
    ResponseSchema(name="justification_symptoms_exploration", description="Justify your answer."),

    ResponseSchema(name="active_listening_empathy_response", description="Did they demonstrate active listening and empathy skills during the interaction? Answer from 1 to 5.", type="int"),
    ResponseSchema(name="justification_active_listening_empathy", description="Justify your answer."),

    ResponseSchema(name="anamnesis_detailing_response", description="Was the anamnesis well-conducted, covering historical, social, family, and medical aspects that could influence the diagnosis? Answer from 1 to 5.", type="int"),
    ResponseSchema(name="justification_anamnesis_detailing", description="Justify your answer."),

    ResponseSchema(name="symptoms_identification_response", description="Did the professional correctly identify the main symptoms and signs of the patient? Answer from 1 to 5.", type="int"),
    ResponseSchema(name="justification_symptoms_identification", description="Justify your answer."),

    ResponseSchema(name="clinical_reasoning_response", description="Did they make logical connections between symptoms and possible diagnoses? Answer from 1 to 5.", type="int"),
    ResponseSchema(name="justification_clinical_reasoning", description="Justify your answer."),

    ResponseSchema(name="diagnosis_accuracy_response", description="Did the client request human or specialist care? Answer from 1 to 5.", type="int"),
    ResponseSchema(name="justification_client_escalation", description="Justify your answer."),

    ResponseSchema(name="service_quality_response", description="Regardless of the diagnosis given, did the psychologist provide good service? Answer from 1 to 5.", type="int"),
    ResponseSchema(name="justification_service_quality", description="Justify your answer."),
]

TEMPLATE = """
Evaluate the psychologist's performance based on the history of conversations with the patient. 
For each of the criteria, provide a rating from 1 to 5, where 1 is very poor and 5 is excellent. 


####### USER PROFILE
{user_profile}

####### DISORDER TO BE EVALUATED
Evaluated disorder: {disorder}
Description: {description} 
Symptom: {symptom}
Diagnosis: {diagnosis}
Treatment: {treatment}


####### CHAT HISTORY
{chat_history}


####### PSYCHOLOGIST'S DIAGNOSIS
{psy_diagnosis}

####### ITEMS TO BE EVALUATED
{format_instructions}

####### ANSWER FORMAT
Return your review in json format
"""

class ExperienceEval:
    def __init__(self, 
                 model_name: str='llama3-8b-8192', 
                 template: str=TEMPLATE, 
                 response_schema: str=RESPONSE_SCHEMA):

        output_parser = StructuredOutputParser.from_response_schemas(response_schema)
        format_instructions = output_parser.get_format_instructions()

        prompt = PromptTemplate(
            template=template,
            input_variables=["user_profile","disorder","description","symptom","diagnosis","treatment","chat_history","psy_diagnosis"],
            partial_variables={"format_instructions": format_instructions}
        )

        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model_name = model_name
        self.prompt = prompt
        self.output_parser = output_parser

    def invoke(self,
               user_profile: str,
               disorder: str,
               description: str,
               symptom: str,
               diagnosis: str,
               treatment: str,
               chat_history: str,
               psy_diagnosis: str
               ):
        formatted_prompt = self.prompt.format(user_profile=user_profile,
                                              disorder=disorder,
                                              description=description,
                                              symptom=symptom,
                                              diagnosis=diagnosis,
                                              treatment=treatment,
                                              chat_history=chat_history,
                                              psy_diagnosis=psy_diagnosis)
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": formatted_prompt}
            ],
            model=self.model_name,
        )

        response = chat_completion.choices[0].message.content
        
        parsed_response = self.output_parser.parse(response)
        return parsed_response