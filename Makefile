.PHONY: build check lint test verify

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHON ?= python3

lint:
	$(PYTHON) "$(ROOT)/scripts/check_unity_contracts.py"

test: lint

build:
	@if command -v unity >/dev/null 2>&1; then \
		unity -batchmode -quit -projectPath "$(ROOT)/UnityTwitter"; \
	else \
		echo "Unity build skipped: unity is not available on this host."; \
	fi

verify: lint test build

check: verify
