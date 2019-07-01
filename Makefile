build:
	docker-compose build

up:
	docker-compose up

test:
	docker-compose exec exercise-toes-web venv/bin/py.test -vv

test-step-1:
	docker-compose exec exercise-toes-web venv/bin/py.test -vv actblue/test_actblue.py::test_mobile_commons_profile_already_exists actblue/test_actblue.py::test_mobile_commons_profile_upload
