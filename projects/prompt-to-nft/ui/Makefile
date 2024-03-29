.phony: run

run:
	@PACKAGE_MANAGER=$$(command -v bun || command -v pnpm || command -v npm); \
	if [ -z $$PACKAGE_MANAGER ]; then \
		echo "No package manager found. Please install bun, pnpm, or npm."; \
		exit 1; \
	fi; \
	echo "Using $$PACKAGE_MANAGER..."; \
	$$PACKAGE_MANAGER install; \
	$$PACKAGE_MANAGER run dev;
