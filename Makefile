.PHONY: build check lint test verify

override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHON ?= python3

lint:
	$(PYTHON) "$(ROOT)/scripts/check_unity_contracts.py"

test: lint
	$(PYTHON) "$(ROOT)/scripts/test_generated_cache_contract.py"
	$(PYTHON) "$(ROOT)/scripts/test_oauth_callback_preflight_contract.py"
	$(PYTHON) "$(ROOT)/scripts/test_oauth_hardening_contract.py"

build:
	@if command -v unity >/dev/null 2>&1; then \
		unity -batchmode -quit -projectPath "$(ROOT)/UnityTwitter"; \
	else \
		echo "Unity build skipped: unity is not available on this host."; \
	fi

verify: lint test build

check: verify
