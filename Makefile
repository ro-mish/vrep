# Variables
VENV_NAME := venv
PYTHON := python3
VENV_BIN := $(VENV_NAME)/bin
VENV_PYTHON := $(VENV_BIN)/python
VENV_PIP := $(VENV_BIN)/pip

# Default target
.PHONY: all
all: install

# Create virtual environment if it doesn't exist
$(VENV_NAME):
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV_NAME)
	@echo "Virtual environment created."

# Install dependencies
.PHONY: install
install: $(VENV_NAME)
	@echo "Activating virtual environment and installing dependencies..."
	@. $(VENV_BIN)/activate && \
		$(VENV_PIP) install --upgrade pip && \
		$(VENV_PIP) install -e .
	@echo "\nInstallation complete! You can now use 'vrep' command."
	@echo "To activate the virtual environment, run: source venv/bin/activate"

# Clean up
.PHONY: clean
clean:
	@echo "Cleaning up..."
	rm -rf build/ dist/ *.egg-info
	@echo "Build artifacts cleaned."

# Deep clean (including virtual environment)
.PHONY: clean-all
clean-all: clean
	@echo "Removing virtual environment..."
	rm -rf $(VENV_NAME)
	@echo "Virtual environment removed."

# Development setup (includes dev dependencies)
.PHONY: dev-install
dev-install: $(VENV_NAME)
	@echo "Installing development dependencies..."
	@. $(VENV_BIN)/activate && \
		$(VENV_PIP) install --upgrade pip && \
		$(VENV_PIP) install -e ".[dev]"
	@echo "\nDevelopment installation complete!"

# Run tests
.PHONY: test
test: $(VENV_NAME)
	@echo "Running tests..."
	@. $(VENV_BIN)/activate && pytest

# Format code
.PHONY: format
format: $(VENV_NAME)
	@echo "Formatting code..."
	@. $(VENV_BIN)/activate && black vrep/

# Lint code
.PHONY: lint
lint: $(VENV_NAME)
	@echo "Linting code..."
	@. $(VENV_BIN)/activate && flake8 vrep/

# Help
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install      - Install vrep in a virtual environment"
	@echo "  make dev-install  - Install vrep with development dependencies"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make clean-all    - Remove build artifacts and virtual environment"
	@echo "  make test         - Run tests"
	@echo "  make format       - Format code using black"
	@echo "  make lint         - Lint code using flake8"
	@echo "  make help         - Show this help message" 