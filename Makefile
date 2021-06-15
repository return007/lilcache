test:
	@echo "Running tests"
	@pytest ./tests/*

install:
	@echo "Installing..."
	@pip install -e .

doc:
	@echo "Generating docs..."
	@rm -rf ./docs/out
	@sphinx-build docs/ docs/out
