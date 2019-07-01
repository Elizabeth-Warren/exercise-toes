# exercise-toes
We believe down to our toes. Generic home for endpoints for organizing APIs, webhooks, website utils, etc.

This is a service running in production, pared down to be an interview
question about implementing an ActBlue webhook that opts new donors into
our text message program.

Start with the documentation for this interview:

https://docs.google.com/document/d/1AVADcuya9Up_wv8WTDn2mIqq3eABN_zXQjHJlBD4ezs/edit

## How to run tests
First:
`make build`
`make up`

Then you can edit code and run tests (no need to `build` or `up` again):
`make test`

As you work on Step 1 of the interview, you can `make test-step-1` to
only run the relevant tests of Step 1. (After they all pass, you should
also check that `make test` still works : )

## How to run locally
1. `make build up`
2. `make up`
3. Open http://0.0.0.0:5000/ locally, e.g. [this mdata/debt endpoint](http://0.0.0.0:5000/dev/mdata/debt?args=120000&profile_techsandbox_income_last_year=120000&profile_techsandbox_outstanding_student_loan_debt=60000)
