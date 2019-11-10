import boto3
import json
import os
from src.response import make_response


def claim(event, context):
    event_body = json.loads(event["body"])

    stack_name = event_body["stackName"]

    client = boto3.client("dynamodb")
    bdd_lock_table = os.environ["BDD_LOCK_TABLE_NAME"]

    try:
        response = client.transact_write_items(
            TransactItems=[
                {
                    "Update": {
                        "TableName": bdd_lock_table,
                        "Key": {"stackName": {"S": stack_name}},
                        "ConditionExpression": "isAvailable = :x",
                        "UpdateExpression": "remove isAvailable",
                        "ExpressionAttributeValues": {":x": {"S": "x"},},
                    }
                }
            ]
        )
    except client.exceptions.TransactionCanceledException:
        return make_response({"error": "Transaction Cancelled"}, 400)

    return make_response(
        {"info": "Successfully claimed stack", "response": response}
    )

