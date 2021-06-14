test:
	@echo "Running tests"
	@pytest ./tests/*

install:
	@echo "Installing..."
	@pip install -e .

