.PHONY: build_frontend
SHELL := /bin/bash

IMAGE_REPOSITORY ?= "samrreynolds4/"
DOCKERFILES ?= "./devops/yordle/dockerfiles"
IMAGE_TAG := $(shell git name-rev --name-only HEAD 2>/dev/null || echo "unknown")
IMAGE_TAG := $(shell git describe --tags --exact-match 2>/dev/null || echo $(IMAGE_TAG))

build_frontend:
	docker buildx build --platform linux/amd64 -t ${IMAGE_REPOSITORY}yordle-frontend:${IMAGE_TAG} -f ${DOCKERFILES}/frontend.dockerfile .

build_backend:
	docker buildx build --platform linux/amd64 -t ${IMAGE_REPOSITORY}yordle-backend:${IMAGE_TAG} -f ${DOCKERFILES}/backend.dockerfile .



push_backend:
	docker push ${IMAGE_REPOSITORY}yordle-backend:${IMAGE_TAG}

push_frontend:
	docker push ${IMAGE_REPOSITORY}yordle-frontend:${IMAGE_TAG}

cicd_push_frontend:

run_frontend:
	docker run --network yordle -it -p 3000:3000 ${IMAGE_REPOSITORY}yordle-frontend:latest
run_backend:
	docker run --network yordle -it -p 8000:8000 ${IMAGE_REPOSITORY}yordle-backend:latest

run:
