DOCKER_ORG := ritualnetwork
EXAMPLE_NAME := tgi-llm-ui
TAG := $(DOCKER_ORG)/example-$(EXAMPLE_NAME)-infernet:latest

.phony: build run publish

build:
	@docker build -t $(TAG) --build-arg index_url=$(index_url) .

run: build
	docker run --env-file ./gradio_ui.env -p 3001:7860 $(TAG)

# You may need to set up a docker builder, to do so run:
# docker buildx create --name mybuilder --bootstrap --use
# refer to https://docs.docker.com/build/building/multi-platform/#building-multi-platform-images for more info
build-multiplatform:
	docker buildx build --platform linux/amd64,linux/arm64 -t $(TAG) --push .
