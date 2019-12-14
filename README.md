<div align="center">
    <img width="400px" src="./logo.png" align="center" alt="BDD Lock Logo">
    <h3>A lock table to claim existing stacks when running BDD tests to reduce CI runtime</h3>
</div>


## Motivation

- Running BDD tests on a microservice often requires creating a standalone stack before you can create and delete dummy data
- Creating brand new stacks for each new build adds a large overhead to your CI runtime (especially with custom domains)
- Updating stacks is significantly faster

Instead you can have some stacks which are ready to go that any CI job can claim, update with their code, run tests and then release back

## How it works

- There is a dynamoDB table like so:

| stackName     | repoName          | isAvailable   | lastUsed              |
| -             | -                 | -             | -                     |
| testStack2192 | paymentService    | x             | 2019-11-20T23:10:28   |
| testStack3244 | paymentService    | x             | 2019-11-19T12:31:43   |
| testStack1295 | emailService      |               | 2019-11-20T14:12:11   |
| testStack9521 | paymentService    |               | 2019-11-20T23:09:49   |
| testStack1295 | emailService      | x             | 2019-11-20T19:54:08   |

- When your CI runs and needs a stack, it checks if there are any available stacks for its repo (`/get-available`)
- If there is:
    - It claims a stack (`/claim-stack`) and marks it as not available (using a transact write to ensure only one job can claim a stack at a time)
    - It then updates the stack with its code and runs its tests
    - After (success or fail) it marks the stack as available again (`/release-stack`)
- If not:
    - It creates a new entry in the table with a random stack name (`/create-stack`)
    - It creates a new stack with this name and runs its tests
    - After (success or fail) it marks the stack as available again (`/release-stack`)
- After your CI has run a number of times, you should have enough stacks created that any new job can always claim an existing stack
- Note: there is also a scheduled `release-unused` lambda which runs at 1am every weekday to release any stack that has been claimed for more than 2 hours
  - This is to clean up from any jobs that exit from your CI before releasing the stack

## Endpoints

- See the [schema](./docs/schema.md)
- Or import the [Postman Collection](./bdd-lock-table.postman_collection.json)
    - Set variables for `bddStack` and `token`

## <a id="deploy"></a>Deploying

- Create a SecureString parameter in your AWS parameter store called `bddLockTableAuthToken`
    - This should be a generated string
- `pipenv install`
- `yarn`
- `yarn sls deploy --stackName {YOUR_STACK_NAME}`

## Setting up on CircleCI

See an [Example repo](https://github.com/robcronin/sls-bdd-python-optimised-ci) with some simple tests

Or see the CircleCI example in the [ci-examples](./ci-examples) directory of this repo

- [Deploy](#deploy) a version of this repo
- Save the following variables in your CI environment
    - `BDD_LOCK_ENDPOINT`: The root of your deployed endpoints e.g. `https://xxxxxxxxxx.execute-api.eu-west-2.amazonaws.com/dev`
    - `BDD_LOCK_AUTH_TOKEN`: The password you generated and stored in ssm
    - `REPO_NAME`: your repo name
- Set up your ci config to use the relevant endpoints to claim a stack or create a new one if none available
    - Consider using a loop to try again if it tries to claim a stack at the same time as another job
- Run your tests against your stack but don't fail the build straight away if they fail
- Release your stack on sucess or failure
- Finish your build with success or failure

## Further Ideas

- Don't release a stack that fails so that the developer can debug on the stack
    - Schedule the stack to be released after x time
- ~~Schedule removal of stacks that haven't been used in x time~~
- Allow update of all existing stacks to a master branch in case of a big change(adding a dynamoDB index for example)