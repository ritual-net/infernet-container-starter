include internal.mk

index_url ?= ''

build-container:
	$(MAKE) -C ./projects/$(project)/container build index_url=$(index_url)

remove-containers:
	docker compose -f deploy/docker-compose.yaml down || true
	docker stop $(project) anvil-node && docker rm $(project) anvil-node || true

build-multiplatform:
	$(MAKE) -C ./projects/$(project)/container build-multiplatform

deploy-container: stop-container
	cp ./projects/$(project)/container/config.json deploy/config.json
	docker compose -f deploy/docker-compose.yaml up -d
	docker logs infernet-node -f

stop-container:
	docker compose -f deploy/docker-compose.yaml kill || true
	docker compose -f deploy/docker-compose.yaml rm -f || true
	docker kill $(project) || true
	docker rm $(project) || true

watch-logs:
	docker compose -f deploy/docker-compose.yaml logs -f

deploy-contracts:
	$(MAKE) -C ./projects/$(project)/contracts deploy

call-contract:
	$(MAKE) -C ./projects/$(project)/contracts call-contract

build-service:
	$(MAKE) -C ./projects/$(project)/$(service) build

run-service:
	$(MAKE) -C ./projects/$(project)/$(service) run
