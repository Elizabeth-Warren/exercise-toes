# exercise-toes
We believe in this fight down to our toes. Generic home for endpoints for organizing APIs, webhooks, website utils, etc.

This is a service running in production, pared down to be an interview
question about implementing an ActBlue webhook that opts new donors into
our text message program.

## How to run tests
First:
`make build up`

Then you can edit code and run tests (no need to `build` or `up` again):
`make test`

As you work on Step 1 of the interview, you can `make test-step-1` to
only run the relevant tests of Step 1. (After they all pass, you should
also check that `make test` still works : )

## How to run locally (not needed for interview)
1. `make build up`
2. Open http://0.0.0.0:5005/
