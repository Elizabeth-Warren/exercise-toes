# toes
We believe down to our toes. Generic home for endpoints for organizing APIs, webhooks, website utils, etc.

## How to run tests
`make test`

## How to run locally
1. `make build`
2. `make up`
3. Open http://0.0.0.0:5000/ locally, e.g. [this mdata/debt endpoint](http://0.0.0.0:5000/dev/mdata/debt?args=120000&profile_techsandbox_income_last_year=120000&profile_techsandbox_outstanding_student_loan_debt=60000)

## How to deploy an update function in the cloud
- `make update-dev`: updates http://toes.elizabethwarren.codes/dev/...

- `make update-prod`: updates http://toes.elizabethwarren.codes/prod/...
This is where prod traffic points to.
