import json
import boto3
from services.service_interface import ServiceInterface

class AwsService(ServiceInterface):
    def __init__(self):
        self.lambda_client = boto3.client('lambda')

    def send_profile(self, profile_data):
        return self._invoke_lambda('lambda_s3_person', profile_data)

    def get_profile_info(self):
        return self._invoke_lambda('lambda_service_predict', {})

    def chat_with_user(self, message):
        return self._invoke_lambda('lambda_service', {'message': message})

    def finalize_evaluation(self, chat_history):
        self._invoke_lambda('lambda_s3_conversation', {'history': chat_history})
        return self._invoke_lambda('lambda_service_result', {})

    def _invoke_lambda(self, function_name, payload):
        # Invoca a Lambda AWS
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            Payload=json.dumps(payload)
        )
        return response['Payload'].read()
