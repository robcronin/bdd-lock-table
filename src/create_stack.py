import json
from src.response import make_response


def create(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
    }
    return make_response(body)
