import boto3
import datetime
import json
import os
from boto3.dynamodb.conditions import Attr
from src.response import make_response
from src.claim_stack import transact_write


def release(event, context):
    bdd_lock_table = os.environ["BDD_LOCK_TABLE_NAME"]
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(bdd_lock_table)

    scan_results = table.scan(
        FilterExpression=Attr("isAvailable").not_exists(),
    )

    num_released = 0
    expiry_seconds = os.environ["EXPIRY_SECONDS"]
    now = datetime.datetime.now()
    for stack in scan_results["Items"]:
        last_used = datetime.datetime.fromisoformat(stack["lastUsed"])
        time_diff = now - last_used
        if time_diff.total_seconds() > int(expiry_seconds):
            transact_write(stack["stackName"], "release")
            num_released += 1

    return make_response({"info": f"Successfully released {num_released} stacks"})
