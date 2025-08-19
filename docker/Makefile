.PHONY: run stop restart

run:
	echo "Running stack mcp server ..."
	docker-compose -p kgrag-mcp-server pull
	docker-compose -p kgrag-mcp-server up -d

stop:
	echo "Stopping mcp server ..."
	docker-compose -p kgrag-mcp-server down

restart: stop run
	echo "All services are restarted"