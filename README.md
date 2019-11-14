# BDD Lock Table

A lock table to claim exitsing stacks when running BDD tests to reduce CI runtime

## Motivation

- Running BDD tests on a microservice tends to require a standalone stack before you make and create dummy data
- Creating brand new stacks for each new build adds a large overhead to your CI runtime (especially with custom domains)
- Updating stakcs is significantly faster
- Instead have some stacks ready to go that any CI job can claim, update with their code, run tests and then release back

## How it works

- There is a dynamoDB table like so:

| stackName     | repoName          | isAvailable   |
| -             | -                 | -             |
| testStack2192 | paymentService    | x             |
| testStack3244 | paymentService    | x             |
| testStack1295 | emailService      |               |
| testStack9521 | paymentService    |               |
| testStack1295 | emailService      | x             |

- When your CI runs and wants to create a stack it checks if there are any available stacks for its repo (`/get-available`)
- If there is:
    - It claims a stack (`/claim-stack`)and marks it as not available (using a transact write to ensure only one job can claim a stack at a time)
    - It then updates the stack with its code and runs its tests
    - After (success or fail) it marks the stack as available again (`/release-stack`)
- If not:
    - It creates a new entry in the table with a random stack name (`/create-stack`)
    - It creates a new stack with this name and runs its tests
    - After (success or fail) it marks the stack as available again (`/release-stack`)
- After your CI has run for a while you should have enough stacks created that any new job can always claim an existing stack

## Deploying

- `yarn`
- `pipenv install`
- `yarn sls deploy --stackName {YOUR_STACK_NAME}`

## Endpoints

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