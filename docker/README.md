# Docker

## Overview

This Docker Compose setup provides a multi-service environment for the `kgrag-mcp-server` application, including logging and monitoring tools.

## Services

- **kgrag-mcp-server**: Main application server. Exposes port `8000`. Requires environment variables for configuration (e.g., API keys, model settings).
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

## Volumes

- `grafana-data`: Persists Grafana data.
- `loki-log`: Used by Promtail for log collection.

## Network

All services are connected via the custom bridge network `kgrag-mcp-network` (subnet: `172.16.99.0/24`).

## Monitoring

Grafana is pre-configured to use Loki as the default data source for log visualization.
