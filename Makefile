build:
	docker build --tag exercise-toes .

up:
	docker run --name exercise-toes-web --volume `pwd`:/app --publish 5005:5005 --rm exercise-toes

test:
	docker exec exercise-toes-web python -m pytest -vv
