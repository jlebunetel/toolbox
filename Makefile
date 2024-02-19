default: help

RED=\033[1;31m
GREEN=\033[1;32m
YELLOW=\033[0;33m
BLUE=\033[1;34m
NC=\033[0m

define message_info
	echo "${BLUE}[INFO]${NC} ${YELLOW}$(1)${NC} -> The command as started..."
endef

define message_ok
	echo "${GREEN}[ OK ]${NC} ${YELLOW}$(1)${NC} -> The command was completed successfully!"
endef

define message_fail
	echo "${RED}[FAIL]${NC} ${YELLOW}$(1)${NC} -> An error occurred during the execution of the command."
endef

define command
	@echo "――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――"
	@$(call message_info,$(1)) \
	&& $(2) \
	&& $(call message_ok,$(1)) \
	|| ($(call message_fail,$(1)) ; exit 1)
endef

.PHONY: venv
venv: ## Creates a virtual environment with Python 3.12.
	@$(call command,"Delete previous venv",\
		rm -rf venv \
	)

	@$(call command,"Create new venv",\
		python3.12 -m venv venv \
	)

.PHONY: upgrade-pip
upgrade-pip:
	@$(call command,"Upgrade pip",\
		venv/bin/pip install \
			--require-virtualenv \
			--upgrade pip \
	)

.PHONY: install
install: upgrade-pip ## Installs project dependencies.
	@$(call command,"Install project dependencies",\
		venv/bin/pip install \
			--require-virtualenv \
			--requirement requirements.txt \
	)

.PHONY: install-dev
install-dev: upgrade-pip ## Installs dev and test dependencies.
	@$(call command,"Install dev and test dependencies",\
	venv/bin/pip install \
		--require-virtualenv \
		--requirement requirements.txt \
		--requirement requirements-dev.txt \
		--requirement requirements-test.txt \
	)

.PHONY: build-requirements
build-requirements: upgrade-pip ## Builds requirements files.
	@$(call command,"Build requirements.txt",\
	venv/bin/pip-compile \
		--output-file=requirements.txt \
		pyproject.toml \
	)

	@$(call command,"Build requirements-dev.txt",\
	venv/bin/pip-compile \
		--extra=dev \
		--output-file=requirements-dev.txt \
		pyproject.toml \
	)

	@$(call command,"Build requirements-test.txt",\
	venv/bin/pip-compile \
		--extra=test \
		--output-file=requirements-test.txt \
		pyproject.toml \
	)

.PHONY: sync-dev
sync-dev: upgrade-pip ## Syncs dev and test requirements.
	@$(call command,"Sync requirements",\
	venv/bin/pip-sync \
		requirements.txt \
		requirements-dev.txt \
		requirements-test.txt \
	)

.PHONY: clean-python
clean-python: ## Cleans Python environment.
	@$(call command,"Delete Python cache files",\
		find . -path "*.pyc" -not -path "./venv*" -delete \
		&& find . -path "*/__pycache__" -not -path "./venv*" -delete \
	)

.PHONY: clean
clean: clean-python ## Cleans project repository.
	@$(call command,"Delete Mypy cache",\
		rm -rf .mypy_cache/ \
	)

	@$(call command,"Delete Pytest cache",\
		rm -rf .pytest_cache/ \
	)

	@$(call command,"Delete Ruff cache",\
		rm -rf .ruff_cache/ \
	)

	@$(call command,"Delete Coverage files",\
		rm -rf htmlcov/ .coverage \
	)

.PHONY: quickstart
quickstart: venv install ## Install and run a demo app.
	@$(call command,"Update database schema",\
		venv/bin/python manage.py migrate \
	)

	@$(call command,"Create a superuser",\
		DJANGO_SUPERUSER_PASSWORD=demo \
		venv/bin/python manage.py \
			createsuperuser \
			--noinput \
			--username demo \
			--email demo@example.com \
	)

	@$(call command,"Start a lightweight web server for development and also serves static files",\
		venv/bin/python manage.py runserver \
	)

.PHONY: help
help: ## Lists all the available commands.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "${BLUE}%-24s${NC} %s\n", $$1, $$2}'
