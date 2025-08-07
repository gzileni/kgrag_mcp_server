.PHONY: run stop restart

run:
	echo "Running stack agent ..."
	docker-compose -p kgrag-agent up -d

stop:
	echo "Stopping qdrant ..."
	docker-compose down

restart: stop run
	echo "All services are restarted"