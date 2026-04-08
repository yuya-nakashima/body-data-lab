.PHONY: setup db-init run-api run-etl test test-integration

setup:
	mkdir -p db etl docs

db-init:
	sqlite3 db/body_data_lab.sqlite3 ".databases"

run-api:
	cd api && go run .

run-etl:
	.venv/bin/python3 -m etl.main

test:
	.venv/bin/python3 -m pytest tests/ -v --ignore=tests/test_notifier_integration.py

test-integration:
	MAILPIT_API_URL=http://localhost:8025 .venv/bin/python3 -m pytest tests/test_notifier_integration.py -v
