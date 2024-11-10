import os
from services.aws_services import AwsService
from services.fake_services import FakeService
from services.local_services import LocalService

def get_service():
    env = os.getenv("ENV", "local")
    if env == "aws":
        return AwsService()
    else:
        return LocalService()
