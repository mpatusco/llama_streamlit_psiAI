from services.service_interface import ServiceInterface

class FakeService(ServiceInterface):
    def send_profile(self, profile_data):
        return {"status": "success"}

    def get_profile_info(self):
        return {"nome": "Teste Usuário"}

    def chat_with_user(self, message, profile):
        return "Resposta simulada."

    def finalize_evaluation(self, chat_history):
        return {"resultado": "Conversa simulada finalizada."}
    
    def get_users(self):
        return [{'username': 'Felipe',
                'age': '32',
                'profession': 'Cientista de dados',
                'mental_disorder': 'Schizophrenia',
                'location': 'São Paulo, Brazil',
                'life_issues': 'não gosta do trabalho porque as pessoas não o entendem',
                'persona': 'Uma pessoa animada que sabe se comunicar. Por algum motivo tenta sempre falar da forma mais formal possível',
                'backstory': 'gosta de tocar guitarra sozinho'},
                {'username': 'Ana',
                'age': '20',
                'profession': 'Designer Gráfico',
                'mental_disorder': 'Depressão',
                'location': 'São Paulo, Brasil',
                'life_issues': 'se sente triste por estar morando sozinha',
                'persona': 'Uma pessoa reservada que não se sente bem conversando com as pessoas',
                'backstory': 'pais moram no interior'}]
