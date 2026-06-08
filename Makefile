.PHONY: lint test build verify

PYTHON ?= python3

lint:
	$(PYTHON) scripts/check_unity_contracts.py

test: lint

build:
	@if command -v unity >/dev/null 2>&1; then \
		unity -batchmode -quit -projectPath UnityTwitter; \
	else \
		echo "Unity build skipped: unity is not available on this host."; \
	fi

verify: lint test build
