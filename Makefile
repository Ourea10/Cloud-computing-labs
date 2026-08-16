install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

up:
	docker compose -f infrastructure/docker/docker-compose.yml up -d

down:
	docker compose -f infrastructure/docker/docker-compose.yml down

logs:
	docker compose -f infrastructure/docker/docker-compose.yml logs -f

localstack-up:
	docker compose -f infrastructure/localstack/docker-compose.yml up -d

localstack-down:
	docker compose -f infrastructure/localstack/docker-compose.yml down