from abc import ABC, abstractmethod
from typing import Dict, Any, List

class ServiceInterface(ABC):
    """
    Interface para definir o serviço de comunicação com lambdas para adição de perfis,
    atendimento com chat e finalização de avaliação.
    """

    @abstractmethod
    def send_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envia os dados do perfil de um novo usuário.

        Args:
            profile_data (Dict[str, Any]): Dicionário contendo as informações do perfil.

        Returns:
            Dict[str, Any]: Resposta do serviço.
        """
        pass

    @abstractmethod
    def get_profile_info(self, info: str=["nome"]) -> Dict[str, Any]:
        """
        Recupera o nome de um usuário para iniciar uma avaliação.

        Returns:
            Dict[str, Any]: Dicionário contendo o nome do usuário.
        """
        pass

    @abstractmethod
    def chat_with_user(self, message: str) -> str:
        """
        Envia uma mensagem para o usuário em atendimento e recebe a resposta.

        Args:
            message (str): Mensagem enviada para o usuário.

        Returns:
            str: Resposta do usuário ou do sistema.
        """
        pass

    @abstractmethod
    def finalize_evaluation(self, chat_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Envia o histórico da conversa para as lambdas de finalização da avaliação.

        Args:
            chat_history (List[Dict[str, Any]]): Lista de mensagens trocadas no atendimento.

        Returns:
            Dict[str, Any]: Resposta do serviço.
        """
        pass
