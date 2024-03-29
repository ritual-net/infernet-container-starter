deploy-container:
	cp ./projects/$(project)/container/config.json deploy/config.json
	cd deploy && docker-compose up

deploy-contracts:
	$(MAKE) -C ./projects/$(project)/contracts deploy

call-contract:
	$(MAKE) -C ./projects/$(project)/contracts call-contract
