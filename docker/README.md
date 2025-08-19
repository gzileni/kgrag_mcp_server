# Docker

## Overview

This [Docker Compose](./docker-compose.yml) setup provides a multi-service environment for the `kgrag-mcp-server` application from image `ghcr.io/gzileni/kgrag_mcp_server:main`, including logging and monitoring tools.

## Services

- **kgrag-mcp-server**: Main application server.  
    - **Ports exposed:**  
        - `8000`: Application  
        - `6379`: Redis  
        - `6333`, `6334`: QDrant  
        - `7474`: HTTP (Neo4j)  
        - `7687`: Bolt (Neo4j)  
    - **Environment variables:**  
        - `APP_ENV`, `LLM_MODEL_TYPE`, `OPENAI_API_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `AWS_BUCKET_NAME`, `COLLECTION_NAME`, `LLM_MODEL_NAME`, `MODEL_EMBEDDING`, `LLM_URL`, `LOKI_URL`
    - **Volumes:**  
        - `qdrant_data:/qdrant/storage:z`  
        - `./qdrant/config.yml:/qdrant/config.yml:ro`  
        - `redis_data:/data`  
        - `neo4j_data:/var/lib/neo4j/data`  
        - `./neo4j.conf:/etc/neo4j/neo4j.conf:ro`
    - **Network:**  
        - Connected to `kgrag-mcp-network`
- **kgrag-mcp-loki**: Grafana Loki instance for log aggregation. Exposes port `3100`.
- **kgrag-mcp-promtail**: Promtail agent for collecting and shipping logs to Loki.
- **kgrag-mcp-grafana**: Grafana dashboard for monitoring and visualizing logs. Exposes port `3000`.

## Usage

1. Clone the repository and navigate to the `docker` directory.
2. Create a `.env` file with the required environment variables.
3. Start the services:
    ```bash
    docker compose up -d
    ```
4. Access:
    - Application: [http://localhost:8000](http://localhost:8000)
    - Grafana: [http://localhost:3000](http://localhost:3000)
    - Redis: [localhost:6379](http://localhost:6379)
    - QDrant: [localhost:6333](http://localhost:6333), [localhost:6334](http://localhost:6334)
    - Neo4j: [http://localhost:7474](http://localhost:7474) (HTTP), [bolt://localhost:7687](bolt://localhost:7687) (Bolt)

## Environment Variables

Set the following variables in your `.env` file:

- `APP_ENV`
- `LLM_MODEL_TYPE`
- `OPENAI_API_KEY`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_BUCKET_NAME`
- `COLLECTION_NAME`
- `LLM_MODEL_NAME`
- `MODEL_EMBEDDING`
- `LLM_URL`
- `LOKI_URL` (default: `http://kgrag-mcp-loki:3100/loki/api/v1/push`)

## Volumes

- `qdrant_data`: Persists QDrant data.
- `redis_data`: Persists Redis data.
- `neo4j_data`: Persists Neo4j data.
- `grafana-data`: Persists Grafana data.
- `loki-log`: Used by Promtail for log collection.

## Network

All services are connected via the custom bridge network `kgrag-mcp-network` (subnet: `172.16.99.0/24`).

## Monitoring

Grafana is pre-configured to use Loki as the default data source for log visualization.

