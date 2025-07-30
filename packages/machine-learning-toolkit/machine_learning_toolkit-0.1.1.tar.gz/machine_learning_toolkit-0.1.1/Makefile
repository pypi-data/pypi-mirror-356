PACKAGE_NAME=machine-learning-toolkit

PYTHON=python

.PHONY: clean build upload install test

## Remove build artifacts
clean:
	rm -rf build dist *.egg-info
	find . -name "__pycache__" -type d -exec rm -r {} +

## Build the distribution packages
build: clean
	$(PYTHON) -m build

## Upload to PyPI (requires twine)
# upload: build
# 	twine upload dist/*

## Install the package locally in editable mode
install:
	$(PYTHON) -m pip install -e .

## Run tests (if you later add a tests/ folder)
test:
	$(PYTHON) -m unittest discover tests

## Help message
help:
	@echo "Makefile commands:"
	@echo "  make clean   - Remove build artifacts"
	@echo "  make build   - Build source and wheel packages"
	@echo "  make install - Install the package locally"
	@echo "  make test    - Run unittests"
