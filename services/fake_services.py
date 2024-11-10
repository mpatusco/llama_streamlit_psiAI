from services.service_interface import ServiceInterface

class FakeService(ServiceInterface):
    def send_profile(self, profile_data):
        return {"status": "success"}

    def get_profile_info(self):
        return {"nome": "Teste Usuário"}

    def chat_with_user(self, message):
        return "Resposta simulada."

    def finalize_evaluation(self, chat_history):
        return {"resultado": "Conversa simulada finalizada."}
