.PHONY: setup run-backend run-tests dvc-repro

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run-backend:
	. .venv/bin/activate && uvicorn src.backend.app.main:app --reload --port 8000

run-tests:
	. .venv/bin/activate && pytest -q

dvc-repro:
	dvc repro
