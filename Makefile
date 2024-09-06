PROJECT_NAME = gpx-utils
VENV_PATH = ~/.venv/$(PROJECT_NAME)

all: venv install

venv:
	@python3 -m venv $(VENV_PATH)

install: venv
	@source $(VENV_PATH)/bin/activate && \
	pip install --disable-pip-version-check -q -r requirements.txt