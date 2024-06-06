DOCKER_ORG := ritualnetwork
EXAMPLE_NAME := prompt-to-nft
TAG := $(DOCKER_ORG)/example-$(EXAMPLE_NAME)-infernet:latest

.phony: build run build-multiplatform

build:
ifdef CI
	mkdir -p wallet # in CI we don't have a wallet directory. This enables to bypass that and ensure that the image
	# is built successfully
endif
	@docker build -t $(TAG) --build-arg index_url=$(index_url) .

wallet_dir ?= /app/wallet

run:
	docker run -p 3000:3000 -v ./wallet:$(wallet_dir) --env-file prompt_to_nft.env $(TAG)

# You may need to set up a docker builder, to do so run:
# docker buildx create --name mybuilder --bootstrap --use
# refer to https://docs.docker.com/build/building/multi-platform/#building-multi-platform-images for more info
build-multiplatform:
	docker buildx build --platform linux/amd64,linux/arm64 -t $(TAG) --push .
