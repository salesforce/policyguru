SHELL:=/bin/bash


.PHONY: clean
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	rm -rf ui/.npmrc ui/.yarnrc
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*.egg-link' -delete
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	name '*~' -exec rm --force  {}

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

.PHONY: lint
lint:
	invoke test.format
	invoke test.lint

.PHONY: run-python-tests
run-python-tests:
	invoke test.security
	invoke unit.pytest

.PHONY: validate
validate:
	cfn-lint template.yaml
	sam validate

.PHONY: run-docker
run-docker:
	docker-compose up -d --build

.PHONY: run
run:
	uvicorn policyguru.main:app --host 0.0.0.0 --port 8080 --reload

.PHONY: deploy
deploy:
	sam build --use-container
	sh ./deploy.sh

