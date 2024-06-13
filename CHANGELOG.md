# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 2.8.0 (2024-06-13)

### Feat

- **frontend**: design system enhancing

## 2.7.0 (2024-04-12)

### Feat

- **dev**: configure docker volume
- **budgets**: minimal app setup
- **api**: install Django REST Framework
- **labbook**: minimal app setup

### Fix

- **budgets**: typo in the description
- **docs**: typo
- **dependencies**: re-build requirements

### Refactor

- **templates**: enhance template menu

## 2.6.3 (2024-03-20)

### Fix

- **typo**: fix some typos

## 2.6.2 (2024-03-20)

### Fix

- **requirements**: update requirements according to pyproject.toml

## 2.6.1 (2024-03-19)

### Fix

- **ci**: rename bandit action

## 2.6.0 (2024-03-19)

### Feat

- **frontend**: upcoming birthdays on the landing page

### Fix

- **ci**: pylint config
- **ci**: pre-commit autoupdate

## 2.5.0 (2024-03-18)

### Feat

- **anniversaries**: send event reminders by emails through manage.py command

## 2.4.2 (2024-03-18)

### Fix

- **vscode**: update vscode settings

## 2.4.1 (2024-03-18)

### Fix

- **settings**: ignore extra environment variables in settings

## 2.4.0 (2024-03-18)

### Feat

- **email**: configure smpt server

## 2.3.1 (2024-03-17)

### Fix

- **ci**: backup before pulling new codebase
- **i18n**: exclude traduction files from .gitignore

## 2.3.0 (2024-03-17)

### Feat

- **i18n**: add french translation files
- **anniversaries**: base models, admin and icalendar generation
- **anniversaries**: minimal app setup

## 2.2.0 (2024-03-06)

### Feat

- **backup**: add backup and restore commands

## 2.1.0 (2024-03-05)

### Feat

- **frontend**: enhance templates with Bulma framework
- **frontend**: add favicon utilities
- **frontend**: add dynamic behavior to the navigation bar

### Fix

- **ci**: update MyPy configuration

### Refactor

- **templates**: move landing page to core app

## 2.0.0 (2024-03-04)

### BREAKING CHANGE

- change the User model

### Feat

- **templates**: enhance templates rendering
- **core**: add core and accounts apps

### Fix

- **ci**: remove ubuntu-latest to run on self-hosted runner

## 1.0.0 (2024-02-21)

### BREAKING CHANGE

- change database engine from SQLite to PostgreSQL

### Feat

- **db**: use PostgreSQL as database engine
- **core**: add PostgreSQL dependencies

### Fix

- **ci**: set postgres host and port env variables
- **ci**: add port redirection to postgres
- **ci**: add env variable to postgres

## 0.4.0 (2024-02-21)

### Feat

- **templates**: add footer to the base template

## 0.3.2 (2024-02-21)

### Fix

- **versioning**: correct version format

## 0.3.1 (2024-02-21)

### Fix

- **versionning**: change version number format and add badges

## 0.3.0 (2024-02-20)

### Feat

- **logging**: set up logging
- **logging**: add json logger and rich dependencies

## 0.2.0 (2024-02-19)

### Feat

- **templates**: add error templates
- **settings**: use pydantic-settings to manage secrets

### Fix

- **pre-commit**: add pydantic to additional_dependencies

## 0.1.0 (2024-02-19)

### Feat

- **static**: collect static files
- **core**: add a minimal Django project

### Fix

- **ci**: remove pre-commit from merge process
- **ci**: change commitizen version_files configuration
- **ci**: fix pre-commit action
- **ci**: fix pre-commit and bumpversion actions

### Perf

- **core**: remove pip-audit from pre-commit
