# Makefile for Python project

# Variables
ENV_NAME = paracuda
PACKAGE_NAME = paracuda
PYTHON_VERSION = 3.9
CONDA_ENV_FILE = environment.yml

# Targets
.PHONY: all create-env install publish clean

# Default target
all: help

# Create Conda environment
create-env:
	@echo "Creating Conda environment..."
	conda env create -f $(CONDA_ENV_FILE)

# Install package
install:
	@echo "Installing the package..."
	conda activate $(ENV_NAME) && \
	pip install .

# Publish package to PyPI
publish:
	@echo "Publishing package to PyPI..."
	conda activate $(ENV_NAME) && \
	python -m build && \
	twine upload dist/*

# Clean up build files
clean:
	@echo "Cleaning up build files..."
	rm -rf build/ dist/ *.egg-info

# Help target
help:
	@echo "Available targets:"
	@echo "  create-env  - Create Conda environment"
	@echo "  install     - Install the package"
	@echo "  publish     - Publish package to PyPI"
	@echo "  release     - Create a GitHub release"
	@echo "  clean       - Clean up build files"
