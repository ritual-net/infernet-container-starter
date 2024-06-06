ifneq ("$(wildcard gcp.env)","")
include gcp.env
endif

get_index_url:
	$(eval token := $(shell gcloud auth print-access-token))
	$(eval index_url := "https://_token:$(token)@$(artifact_location)-python.pkg.dev/$(gcp_project)/$(artifact_repo)/simple")

generate-uv-env-file: get_index_url
	@echo "`echo $(export_prefix)`UV_EXTRA_INDEX_URL=$(index_url)" > uv.env
