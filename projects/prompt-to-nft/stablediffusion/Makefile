DOCKER_ORG := ritualnetwork
EXAMPLE_NAME := stablediffusion
TAG := $(DOCKER_ORG)/example-$(EXAMPLE_NAME)-infernet:latest

.phony: build run build-multiplatform

build:
	@docker build -t $(TAG) --build-arg index_url=$(index_url) .

port_mapping ?= 0.0.0.0:3002:3000

run:
	docker run -p $(port_mapping) --gpus all -v ~/.cache:/root/.cache $(TAG)

# You may need to set up a docker builder, to do so run:
# docker buildx create --name mybuilder --bootstrap --use
# refer to https://docs.docker.com/build/building/multi-platform/#building-multi-platform-images for more info
build-multiplatform:
	docker buildx build --platform linux/amd64,linux/arm64 -t $(TAG) --push .
