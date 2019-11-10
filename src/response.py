import json

def make_response(body, statusCode=200):
    return {
        "statusCode": statusCode,
        "body": json.dumps(body)
    }