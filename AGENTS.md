# Project: django-turbo-helper

## Overview
Django package providing Hotwire/Turbo helpers inspired by Rails. The package supports Turbo Streams, Turbo Frames, and real-time updates through Django Channels.

## Project Structure
- **Source code**: `src/turbo_helper/`
- **Tests**: `tests/`
- **Documentation**: `docs/`

## Available Commands

### Testing
- Run all tests: `tox`
- Run specific tests: `pytest tests/`
- Run tests with verbose output: `pytest -v tests/`

### Code Quality
- Run all pre-commit hooks (black, isort, flake8, mypy): `pre-commit run --all-files`
- Format code: `black src/ tests/`
- Sort imports: `isort src/ tests/`
- Lint code: `flake8 src/ tests/`
- Type check: `mypy src/`

### Building
- Build package: `poetry build`
- Publish to PyPI: `poetry publish`

## Key Components
- `stream.py`: TurboStream actions and responses
- `response.py`: Custom HTTP responses (TurboStreamResponse, HttpResponseSeeOther)
- `signals.py`: Model commit signal decorators
- `shortcuts.py`: Response shortcuts (redirect_303, respond_to)
- `middleware.py`: Request middleware for current request tracking
- `turbo_power.py`: Extended Turbo Stream actions
- `channels/`: Django Channels integration for real-time updates
- `templatetags/`: Django template tags for Turbo

## Configuration Files
- **Dependency management**: `pyproject.toml` (Poetry)
- **Code style**: `setup.cfg` (black, isort, flake8, mypy)
- **Testing**: `tox.ini`, `requirements-dev.txt`
- **Pre-commit hooks**: `.pre-commit-config.yaml`

## Notes
- Python version: >= 3.10
- Django version: >= 5.2
- When committing, all pre-commit hooks will run automatically
- Tests run on multiple Python and Django versions via tox
