.phony: run

volume ?= $(PWD)/data
model ?= mistralai/Mistral-7B-v0.1

run:
	docker run --gpus all --shm-size 1g -p 8080:80 -v $(volume):/data \
		ghcr.io/huggingface/text-generation-inference:1.4 --model-id $(model)
