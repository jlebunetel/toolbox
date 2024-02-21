# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
