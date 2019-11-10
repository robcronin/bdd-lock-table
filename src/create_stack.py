import boto3
import json
import os
from src.response import make_response


def create(event, context):
    event_body = json.loads(event["body"])
    new_stack = {
        "stackName": {"S": event_body["stackName"]},
        "repoName": {"S": event_body["repoName"]},
    }
    if(event_body["isAvailable"]):
        new_stack["isAvailable"] = {"S": "x"}



    client = boto3.client('dynamodb')
    bdd_lock_table = os.environ["BDD_LOCK_TABLE_NAME"]
    try:
        client.put_item(
            TableName=bdd_lock_table,
            Item=new_stack,
            ConditionExpression="attribute_not_exists(stackName)",
        )
    except client.exceptions.ConditionalCheckFailedException:
        return make_response({"error": "Stack Name already exists"}, 400)
    except Exception:
        return make_response({"error": "Unknown Error"}, 400)

    return make_response({"info": "Successfully created stack entry"})
