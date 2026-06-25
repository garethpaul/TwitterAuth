.DEFAULT_GOAL := check
.PHONY: __repository-make-authority build check lint root-test test verify
.SECONDEXPANSION:

ifeq ($(origin PYTHON),undefined)
override PYTHON := /usr/bin/python3
else
override PYTHON := $(value PYTHON)
endif
export PYTHON
UNITY ?=
override UNITY := $(value UNITY)
export UNITY
override REPOSITORY_MAKE_DOLLAR := $$
override REPOSITORY_MAKE_OPEN := (
ifneq ($(findstring $(REPOSITORY_MAKE_DOLLAR)$(REPOSITORY_MAKE_OPEN),$(value PYTHON)),)
$(error PYTHON must be a literal executable path, not Make syntax)
endif
ifneq ($(findstring $(REPOSITORY_MAKE_DOLLAR){,$(value PYTHON)),)
$(error PYTHON must be a literal executable path, not Make syntax)
endif
override SHELL := /bin/sh
override .SHELLFLAGS := -c
build check lint root-test test verify __repository-make-authority: override SHELL := /bin/sh
build check lint root-test test verify __repository-make-authority: override .SHELLFLAGS := -c

ifneq ($(filter command line,$(origin MAKEFLAGS)),)
$(error MAKEFLAGS must not be overridden for repository verification)
endif
override REPOSITORY_MAKE_FIRST_FLAGS := $(firstword $(MAKEFLAGS))
ifneq ($(filter -%,$(REPOSITORY_MAKE_FIRST_FLAGS)),)
override REPOSITORY_MAKE_FIRST_FLAGS :=
endif
override REPOSITORY_MAKE_SHORT_FLAGS := $(REPOSITORY_MAKE_FIRST_FLAGS) $(filter-out --%,$(filter -%,$(MAKEFLAGS)))
ifneq ($(findstring n,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring t,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring q,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring i,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(filter --just-print --dry-run --recon --touch --question --ignore-errors,$(MAKEFLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(strip $(MAKEFILES)),)
$(error MAKEFILES must be empty; repository verification requires this Makefile to be loaded alone)
endif
override MAKEFILES :=
ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override REPOSITORY_MAKEFILE_LIST := $(value MAKEFILE_LIST)
override ROOT := $(shell path='$(subst ','"'"',$(value MAKEFILE_LIST))'; path=$$(printf '%s' "$$path" | /usr/bin/sed 's/^ //'); [ -f "$$path" ] || exit 1; directory=$$(/usr/bin/dirname -- "$$path"); CDPATH= cd -- "$$directory" && /bin/pwd -P)
export ROOT
ifeq ($(strip $(ROOT)),)
$(error repository Makefile path could not be resolved)
endif
override REPOSITORY_SHELL_LITERAL = $(subst $$,$$$$,$(subst ','"'"',$1))
override REPOSITORY_PARSE_SHELL_LITERAL = $(subst ','"'"',$1)
override REPOSITORY_ROOT_LITERAL := $(call REPOSITORY_SHELL_LITERAL,$(ROOT))
override REPOSITORY_PYTHON_LITERAL := $(call REPOSITORY_SHELL_LITERAL,$(PYTHON))
override REPOSITORY_UNITY_LITERAL := $(call REPOSITORY_SHELL_LITERAL,$(UNITY))
override REPOSITORY_PYTHON_IS_VALID := $(shell candidate='$(call REPOSITORY_PARSE_SHELL_LITERAL,$(PYTHON))'; /bin/expr "$$candidate" : '^/' >/dev/null && [ -x "$$candidate" ] && /usr/bin/printf '%s' yes)
ifneq ($(REPOSITORY_PYTHON_IS_VALID),yes)
$(error PYTHON must be an absolute executable path)
endif
ifneq ($(strip $(UNITY)),)
override REPOSITORY_UNITY_IS_VALID := $(shell candidate='$(call REPOSITORY_PARSE_SHELL_LITERAL,$(UNITY))'; /bin/expr "$$candidate" : '^/' >/dev/null && [ -x "$$candidate" ] && /usr/bin/printf '%s' yes)
ifneq ($(REPOSITORY_UNITY_IS_VALID),yes)
$(error UNITY must be an absolute executable path)
endif
endif

build check lint root-test test verify:: $$(if $$(filter file,$$(origin MAKEFILE_LIST)),,$$(error MAKEFILE_LIST must not be overridden))
build check lint root-test test verify:: $$(if $$(filter-out $$(REPOSITORY_MAKEFILE_LIST),$$(value MAKEFILE_LIST)),$$(error repository Makefile must be loaded alone))
build check lint root-test test verify:: $$(if $$(filter-out $$(value MAKEFILE_LIST),$$(REPOSITORY_MAKEFILE_LIST)),$$(error repository Makefile must be loaded alone))
build check lint root-test test verify:: __repository-make-authority

__repository-make-authority::
	@:

define REPOSITORY_PUBLIC_RECIPES
lint::
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/check_unity_contracts.py'

test:: lint
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_generated_cache_contract.py'
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_authentication_only_scene_contract.py'
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_oauth_callback_preflight_contract.py'
	REPOSITORY_PYTHON='$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/run-python.sh' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_oauth_hardening_contract.py'

build::
	@if [ -n '$(REPOSITORY_UNITY_LITERAL)' ]; then \
		'$(REPOSITORY_UNITY_LITERAL)' -batchmode -quit -projectPath '$(REPOSITORY_ROOT_LITERAL)/UnityTwitter'; \
	else \
		echo "Unity build skipped: set UNITY to an absolute editor executable to enable it."; \
	fi

root-test::
	/bin/sh '$(REPOSITORY_ROOT_LITERAL)/scripts/test-makefile-root.sh'

verify:: root-test lint test build

check:: verify
endef
$(eval $(REPOSITORY_PUBLIC_RECIPES))
