#!/bin/bash
./venv/bin/python -m coverage report -m --omit 'venv/*'
./venv/bin/python -m coverage html --omit 'venv/*' -d docs/coverage-report