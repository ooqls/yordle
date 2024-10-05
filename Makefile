.PHONY: build_frontend
SHELL := /bin/bash

IMAGE_REPOSITORY ?= "samrreynolds4/"

build_frontend:
	docker build -t ${IMAGE_REPOSITORY}yordle-frontend:latest -f ./devops/dockerfiles/frontend.dockerfile .

build_backend:
	docker build -t ${IMAGE_REPOSITORY}yordle-backend:latest -f ./devops/dockerfiles/backend.dockerfile .

push_backend:
	docker push ${IMAGE_REPOSITORY}yordle-backend:latest

push_frontend:
	docker push ${IMAGE_REPOSITORY}yordle-frontend:latest

run_frontend:
	docker run --network yordle -it -p 3000:3000 ${IMAGE_REPOSITORY}yordle-frontend:latest
run_backend:
	docker run --network yordle -it -p 8000:8000 ${IMAGE_REPOSITORY}yordle-backend:latest

run:
