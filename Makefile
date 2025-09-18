.PHONY: install setup format test php-lint lint

install: setup

setup:
	python3 -m tools.venv_setup

format:
	black src modules tools tests

test:
	pytest

php-lint:
	python -m tools.php_syntax_check --allow-missing-php

lint: format test php-lint
