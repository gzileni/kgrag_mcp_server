.PHONY: run stop restart dev

PLATFORM ?= cpu

ifeq ($(filter $(PLATFORM),cpu gpu),)
$(error PLATFORM must be 'cpu' or 'gpu' (got '$(PLATFORM)'))
endif

dev:
	@echo "Running stack mcp server ... "
	@docker-compose -p kgrag-mcp-server --profile dev up -d

run:
	@echo "Running stack mcp server ... (platform=$(PLATFORM))"
	@docker-compose -p kgrag-mcp-server --profile all --profile $(PLATFORM) pull
	@docker-compose -p kgrag-mcp-server --profile all --profile $(PLATFORM) up -d

stop:
	@echo "Stopping mcp server ... (platform=$(PLATFORM))"
	@docker-compose -p kgrag-mcp-server --profile all --profile $(PLATFORM) down

restart: stop run
	@echo "All services are restarted (platform=$(PLATFORM))"