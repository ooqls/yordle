.PHONY: run
SHELL := /bin/bash
run:
	uvicorn main:api --reload
test:
	find . -name '*_test.py' | xargs -n 1 python -m unittest