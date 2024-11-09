class FormValidator:
    def __init__(self, required_fields):
        """
        Inicializa o validador com os campos obrigatórios.
        
        Args:
            required_fields (list): Lista de campos obrigatórios para validação.
        """
        self.required_fields = required_fields

    def validate(self, form_data):
        """
        Valida se todos os campos obrigatórios estão preenchidos.

        Args:
            form_data (dict): Dicionário com os dados do formulário.

        Returns:
            tuple: (bool, str) - Retorna True e uma mensagem vazia se válido, 
                                  caso contrário, False e uma mensagem de erro.
        """
        missing_fields = [field for field in self.required_fields if not form_data.get(field)]
        if missing_fields:
            return False, f"Por favor, preencha todos os campos obrigatórios: {', '.join(missing_fields)}"
        return True, ""
