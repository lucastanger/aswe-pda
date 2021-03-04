#!/bin/bash
./venv/bin/python -m pytest --cov=src --cov-report=html:docs/coverage-report tests/
