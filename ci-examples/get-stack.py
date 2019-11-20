import json
import os
import random
import requests

REPO_NAME = os.environ["REPO_NAME"]

headers = {"Authorization": os.environ["BDD_LOCK_AUTH_TOKEN"]}

stack_name = None

while not stack_name:
    available_resp = requests.get(
        os.environ["BDD_LOCK_ENDPOINT"] + "/get-available/" + REPO_NAME, headers=headers
    )
    available_stacks = json.loads(available_resp.text).get("results")

    if len(available_stacks) == 0:
        stack_name = "circle" + str(random.randrange(1000000))
        create_resp = requests.post(
            os.environ["BDD_LOCK_ENDPOINT"] + "/create-stack",
            headers=headers,
            json={
                "stackName": stack_name,
                "repoName": REPO_NAME,
                "isAvailable": False,
            },
        )

    else:
        for stack in available_stacks:
            claim_resp = requests.put(
                os.environ["BDD_LOCK_ENDPOINT"]
                + "/claim-stack/"
                + stack.get("stackName"),
                headers=headers,
                data={
                    "stackName": stack_name,
                    "repoName": REPO_NAME,
                    "isAvailable": False,
                },
            )
            claim_resp_body = json.loads(claim_resp.text)
            if claim_resp_body.get("info") == "Successfully claimed stack":
                stack_name = stack.get("stackName")
                break

print(stack_name)
