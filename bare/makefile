SHELL := /bin/bash
PACKAGE_SLUG=bare
PYTHON_VERSION := $(shell cat .python-version)
PYTHON_SHORT_VERSION := $(shell echo $(PYTHON_VERSION) | grep -o '[0-9].[0-9]*')

ifeq ($(USE_SYSTEM_PYTHON), true)
	PYTHON_PACKAGE_PATH:=$(shell python -c "import sys; print(sys.path[-1])")
	PYTHON_ENV :=
	PYTHON := python
	PYTHON_VENV :=
	UV := uv
else
	PYTHON_PACKAGE_PATH:=.venv/lib/python$(PYTHON_SHORT_VERSION)/site-packages
	PYTHON_ENV :=  . .venv/bin/activate &&
	PYTHON := . .venv/bin/activate && python
	PYTHON_VENV := .venv
	UV := uv
endif

# Used to confirm that uv has run at least once
PACKAGE_CHECK:=$(PYTHON_PACKAGE_PATH)/build
PYTHON_DEPS := $(PACKAGE_CHECK)


.PHONY: all
all: $(PACKAGE_CHECK)

.PHONY: install
install: uv $(PYTHON_VENV) sync

.venv:
	$(UV) venv --python $(PYTHON_VERSION)

.PHONY: uv
uv:
	@command -v uv >/dev/null 2>&1 || { echo >&2 "uv is not installed. Installing via pip..."; pip install uv; }

.PHONY: sync
sync: $(PYTHON_VENV) uv.lock
	$(UV) sync --group dev

$(PACKAGE_CHECK): $(PYTHON_VENV) uv.lock
	$(UV) sync --group dev

uv.lock: pyproject.toml
	$(UV) lock

.PHONY: pre-commit
pre-commit:
	pre-commit install

#
# Formatting
#
.PHONY: chores
chores: ruff_fixes black_fixes dapperdata_fixes tomlsort_fixes

.PHONY: ruff_fixes
ruff_fixes:
	$(UV) run ruff check . --fix

.PHONY: black_fixes
black_fixes:
	$(UV) run ruff format .

.PHONY: dapperdata_fixes
dapperdata_fixes:
	$(UV) run python -m dapperdata.cli pretty . --no-dry-run

.PHONY: tomlsort_fixes
tomlsort_fixes:
	$(PYTHON_ENV) tombi format $$(find . -not -path "./.venv/*" -name "*.toml")

#
# Testing
#
.PHONY: tests
tests: install pytest ruff_check black_check mypy_check dapperdata_check tomlsort_check

.PHONY: pytest
pytest:
	$(UV) run pytest --cov=./${PACKAGE_SLUG} --cov-report=term-missing tests

.PHONY: pytest_loud
pytest_loud:
	$(UV) run pytest --log-cli-level=DEBUG -log_cli=true --cov=./${PACKAGE_SLUG} --cov-report=term-missing tests

.PHONY: ruff_check
ruff_check:
	$(UV) run ruff check

.PHONY: black_check
black_check:
	$(UV) run ruff format . --check

.PHONY: mypy_check
mypy_check:
	$(UV) run mypy ${PACKAGE_SLUG}

.PHONY: dapperdata_check
dapperdata_check:
	$(UV) run python -m dapperdata.cli pretty .

.PHONY: tomlsort_check
tomlsort_check:
	$(PYTHON_ENV) tombi lint $$(find . -not -path "./.venv/*" -name "*.toml")
	$(PYTHON_ENV) tombi format $$(find . -not -path "./.venv/*" -name "*.toml") --check



#
# Dependencies
#

.PHONY: lock
lock:
	$(UV) lock --upgrade

.PHONY: lock-check
lock-check:
	$(UV) lock --check


#
# Packaging
#

.PHONY: build
build: $(PACKAGE_CHECK)
	$(UV) run python -m build
