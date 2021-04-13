#!/bin/bash
python -m pytest --cov=. --cov-report=xml --cov-report html:docs/coverage --cov-report term tests/
