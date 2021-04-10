#!/bin/bash
python -m pytest --cov=src --cov-report=xml --cov-report html:docs/coverage --cov-report term tests/services/test_news_service.py
