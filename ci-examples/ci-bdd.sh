#!/bin/bash

set -e

# Get a stack from the lock table
STACK_NAME=$(pipenv run python get-stack.py)

# Deploy the new code to the stack
yarn deploy --stackName $STACK_NAME

# Run BDD tests on the stack (but don't quit on error yet)
set +e
yarn test:bdd
BDD_SUCCESS=$?
set -e

# Release the stack for other jobs
curl -X PUT "${BDD_LOCK_ENDPOINT}/release-stack/${STACK_NAME}" -H "Authorization: ${BDD_LOCK_AUTH_TOKEN}"

# Return success or failure
exit $BDD_SUCCESS
