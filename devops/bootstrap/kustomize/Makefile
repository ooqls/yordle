KUSTOMIZE = kustomize
BASE_DIR = ./base

.PHONY: apply

apply:
	$(KUSTOMIZE) build $(BASE_DIR) | kubectl apply -f -