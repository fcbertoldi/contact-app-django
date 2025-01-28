VENV_NAME = contact-app-django
PYTHON_VERSION = python3.11
UV_TOOL := $(shell command -v uv)

ifeq ($(UV_TOOL),)
	PIP_CMD := pip
	PIP_COMPILE := pip-compile
	PIP_SYNC := pip-sync --pip-args "--no-deps"
else
	PIP_CMD := uv
	PIP_COMPILE := $(UV_TOOL) pip compile
	PIP_SYNC := $(UV_TOOL) pip sync
endif


build-venv:
	pew new -p=$(PYTHON_VERSION) -c $(PIP_CMD) -a . -r requirements.txt $(VENV_NAME)


lock: requirements.txt


sync:
	pew in $(VENV_NAME) $(PIP_SYNC) requirements.txt


runserver:
	pew in $(VENV_NAME) python manage.py runserver


test:
	pew in $(VENV_NAME) pytest .


django-check:
	pew in $(VENV_NAME) python manage.py check


black:
	pew in $(VENV_NAME) black .


ruff-check:
	ruff check .


ruff-fix:
	ruff check --fix .


bandit:
	bandit -c pyproject.toml -r .


%.txt: %.in
	pew in $(VENV_NAME) $(PIP_COMPILE) --generate-hashes --output-file $@ $<


.PHONY: lock sync build-venv runserver test django-check black ruff-check ruff-fix bandit
