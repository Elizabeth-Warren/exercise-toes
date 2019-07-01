build:
	docker-compose build

up:
	docker-compose up

test:
	docker-compose exec web venv/bin/py.test -vv

update-dev:
	docker-compose run --rm web bash -c 'source /root/.bashrc && invoke update-dev'

update-prod:
	docker-compose run --rm web bash -c 'source /root/.bashrc && invoke update-prod'

tail:
	docker-compose run --rm web bash -c 'source /root/.bashrc && invoke tail'
