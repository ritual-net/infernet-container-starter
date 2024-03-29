DOCKER_ORG := ritualnetwork
TAG := $(DOCKER_ORG)/hello-world-infernet:latest

.phony: build run publish

build:
	@docker build -t $(TAG) .

update-tag:
	jq  ".containers[0].image = \"$(TAG)\"" config.json > updated_config.json && mv updated_config.json config.json

run: build
	docker run \
		-p 3000:3000 $(TAG)

# You may need to set up a docker builder, to do so run:
# docker buildx create --name mybuilder --bootstrap --use
# refer to https://docs.docker.com/build/building/multi-platform/#building-multi-platform-images for more info
build-multiplatform:
	docker buildx build --platform linux/amd64,linux/arm64 -t $(TAG) --push .
