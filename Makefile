

run:
	cd docker && docker compose up --build

test:
	cd docker && docker compose run --rm consumer-tests
	cd docker && docker compose run --rm producer-tests

k3d-import:
	k3d image import docker-producer:latest docker-consumer:latest
