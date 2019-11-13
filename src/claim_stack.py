import boto3
import json
import os
from src.response import make_response


def transact_write(stack_name, update_type):

    client = boto3.client("dynamodb")
    bdd_lock_table = os.environ["BDD_LOCK_TABLE_NAME"]

    update_body = {
        "TableName": bdd_lock_table,
        "Key": {"stackName": {"S": stack_name}},
        "ExpressionAttributeValues": {":x": {"S": "x"},},
    }

    if update_type == "claim":
        update_body["ConditionExpression"] = "isAvailable = :x"
        update_body["UpdateExpression"] = "remove isAvailable"
    elif update_type == "release":
        update_body[
            "ConditionExpression"
        ] = "attribute_not_exists(isAvailable) AND attribute_exists(stackName)"
        update_body["UpdateExpression"] = "set isAvailable = :x"

    try:
        response = client.transact_write_items(TransactItems=[{"Update": update_body}])
    except client.exceptions.TransactionCanceledException:
        return make_response({"error": "Transaction Cancelled"}, 400)

    return make_response(
        {"info": f"Successfully {update_type}ed stack", "response": response}
    )


def claim(event, context):
    stack_name = event.get("pathParameters").get("stackName")
    return transact_write(stack_name, "claim")


def release(event, context):
    stack_name = event.get("pathParameters").get("stackName")
    return transact_write(stack_name, "release")
