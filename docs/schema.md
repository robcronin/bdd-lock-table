# Schema

- `/get-available`
    - `GET` to `{SERVICE_ENDPOINT}/get-available/{REPO_NAME}` returns
    ```json
    {
        "info": "Successfully queried",
        "results": [
            {
                "repoName": "sls-bdd",
                "stackName": "testStack94392",
                "isAvailable": "x"
            },
            {
                "repoName": "sls-bdd",
                "stackName": "testStack12143",
                "isAvailable": "x"
            }
        ]
    }
    ```
- `/claim-stack`
    - `PUT` to `{SERVICE_ENDPOINT}/claim-stack/{STACK_NAME}` returns
    ```json
    {
        "info": "Successfully claimed stack",
    }
    ```
- `/release-stack`
    - `PUT` to `{SERVICE_ENDPOINT}/release-stack/{STACK_NAME}` returns
    ```json
    {
        "info": "Successfully releaseed stack",
    }
    ```
- `/create-stack`
    - `POST` to `{SERVICE_ENDPOINT}/create-stack` with
    ```json
    {
        "stackName": "testStack19038",
        "repoName": "sls-bdd",
        "isAvailable": true
    }
    ```
    returns
    ```json
    {
        "info": "Successfully created stack entry"
    }
    ```