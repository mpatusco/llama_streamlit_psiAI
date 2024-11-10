import json
import boto3
from services.service_interface import ServiceInterface

class AwsService(ServiceInterface):
    def __init__(self):
        self.lambda_client = boto3.client('lambda')

    def send_profile(self, profile_data):
        return self.send_request('lambda_s3_person', profile_data)

    def get_profile_info(self):
        return self.send_request('lambda_service_predict', {})

    def chat_with_user(self, message, profile):
        return self.send_request('lambda_service', {'message': message})

    def finalize_evaluation(self, chat_history):
        self.send_request('lambda_s3_conversation', {'history': chat_history})
        return self.send_request('lambda_service_result', {})

    def send_request(self, function_name, payload):
        # Invoca a Lambda AWS
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            Payload=json.dumps(payload)
        )
        return response['Payload'].read()
    
    def get_users(self):
        return self.send_request('get_users', {})
