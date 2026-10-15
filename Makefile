PYTHON ?= python

clean: clean-eggs clean-build clean-htmlcov
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete

clean-htmlcov:
	@rm -fr htmlcov

clean-eggs:
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

lint:
	pre-commit run -av

pip-dev:
	$(PYTHON) -m pip install -r requirements-dev.txt

test:
	$(PYTHON) -m pytest

build: clean
	$(PYTHON) -m build

release: build
	git tag `$(PYTHON) setup.py -q version`
	git push origin `$(PYTHON) setup.py -q version`
	$(PYTHON) -m twine upload dist/*
