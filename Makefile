PYTHON=python3

.PHONY: dep run run-tests build clean lint

dep: requirements.txt
	@$(PYTHON) -m venv venv
	. venv/bin/activate; \
	python -m pip install --quiet -r requirements.txt; \
	deactivate;

run: dep
	. venv/bin/activate; \
	python main.py; \
	deactivate;

run-tests:
	. venv/bin/activate; \
	pytest tests/*.py; \
	deactivate;

build: dep clean
	. venv/bin/activate; \
	pyinstaller --name qs_dashboard --onefile main.py; \
	deactivate;

wheel: dep clean
	. venv/bin/activate; \
	python setup.py bdist_wheel; \
	pip wheel -r requirements.txt; \
	deactivate;

clean:
	rm -rf dist build __pycache__ qs_dashboard.spec *.whl *.egg-info .pytest_* */__pycache__

flake:
	. venv/bin/activate; \
	flake8 --ignore="F821,W503,F401,E128" qs_dashboard; \
	deactivate;