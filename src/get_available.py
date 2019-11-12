import boto3
import json
import os
from src.response import make_response
from boto3.dynamodb.conditions import Key



def query(event, context):
    repo_name = event.get("pathParameters").get("repoName")

    bdd_lock_table = os.environ["BDD_LOCK_TABLE_NAME"]
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(bdd_lock_table)

    results = table.query(
        IndexName="availableByRepoIndex",
        KeyConditionExpression=Key("repoName").eq(repo_name),
    )

    return make_response({"info": "Successfully queried", "results": results["Items"]})