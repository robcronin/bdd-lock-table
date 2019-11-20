import os


def makeResource(resource):
    return resource[: resource.find("/") + 1] + "*"


def makeAuthResponse(accessType, resource):
    return {
        "principalId": "user",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": accessType,
                    "Resource": makeResource(resource),
                }
            ],
        },
    }


def authorize(event, context):
    passedToken = event["authorizationToken"]
    requiredToken = os.environ["BDD_LOCK_TABLE_AUTH_TOKEN"]
    resource = event["methodArn"]

    if requiredToken and requiredToken == passedToken:
        return makeAuthResponse("Allow", resource)
    return makeAuthResponse("Deny", resource)
