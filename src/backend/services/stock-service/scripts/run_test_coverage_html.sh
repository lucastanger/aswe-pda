#!/bin/bash
pytest --cov-report html --cov=.
echo "To open html report open file: ./htmlcov/index.html"
