.PHONY: up down backend-run backend-seed backend-test frontend-dev install

COMPOSE := $(shell if command -v podman >/dev/null 2>&1; then echo "podman compose"; else echo "docker compose"; fi)

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

install:
	# install backend deps
	python3 -m pip install -r backend/requirements.txt
	# install frontend deps
	cd frontend && npm install

backend-run:
	cd backend && python3 run.py

backend-seed:
	cd backend && python3 scripts/seed.py

backend-test:
	cd backend && PYTHONPATH=. python3 -m pytest -q

frontend-dev:
	cd frontend && npm run dev
