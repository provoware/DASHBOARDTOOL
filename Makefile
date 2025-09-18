.PHONY: install format test php-lint lint

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements-dev.txt

format:
	black src modules tools tests

test:
	pytest

php-lint:
	python -m tools.php_syntax_check --allow-missing-php

lint: format test php-lint
