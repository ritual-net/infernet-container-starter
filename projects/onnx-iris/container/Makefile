DOCKER_ORG := ritualnetwork
EXAMPLE_NAME := onnx-iris
TAG := $(DOCKER_ORG)/example-$(EXAMPLE_NAME)-infernet:latest

.phony: build run build-multiplatform

build:
	@docker build -t $(TAG) --build-arg index_url=$(index_url) .

run:
	docker run -p 3000:3000 $(TAG)

# You may need to set up a docker builder, to do so run:
# docker buildx create --name mybuilder --bootstrap --use
# refer to https://docs.docker.com/build/building/multi-platform/#building-multi-platform-images for more info
build-multiplatform:
	docker buildx build --platform linux/amd64,linux/arm64 -t $(TAG) --push .
