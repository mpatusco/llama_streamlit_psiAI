import os
from services.aws_services import AwsService
from services.fake_services import FakeService

def get_service():
    env = os.getenv("ENV", "local")
    if env == "aws":
        return AwsService()
    else:
        return FakeService()
