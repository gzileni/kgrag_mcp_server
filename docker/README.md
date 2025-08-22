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
        - `redis_data:/data`  
        - `neo4j_data:/var/lib/neo4j/data`  
    - **Network:**  
        - Connected to `kgrag-mcp-network`
- **kgrag-mcp-loki**: Grafana Loki instance for log aggregation. Exposes port `3100`.
- **kgrag-mcp-promtail**: Promtail agent for collecting and shipping logs to Loki.
- **kgrag-mcp-grafana**: Grafana dashboard for monitoring and visualizing logs. Exposes port `3000`.

### Description of variables 

- `APP_ENV`  
    Application environment. Typical values: `production`, `development`, `staging`. Affects logging, configuration and runtime behavior.

- `USER_AGENT`  
    Identifier used in HTTP requests (User-Agent). Use a descriptive value to help trace requests.

- `OPENAI_API_KEY`  
    API key for OpenAI (or compatible provider). Secret: do not commit to a public repository. Format: alphanumeric string.

- `AWS_ACCESS_KEY_ID`  
    AWS access key ID for S3 operations. Secret: do not commit. Format: string.

- `AWS_SECRET_ACCESS_KEY`  
    AWS secret access key for S3. Secret: do not commit. Format: string.

- `AWS_REGION`  
    AWS region where the bucket resides (e.g. `eu-central-1`).

- `AWS_BUCKET_NAME`  
    Name of the S3 bucket used for storing data/assets.

- `COLLECTION_NAME`  
    Name of the collection used in Qdrant or another vector DB to store vectors.

- `VECTORDB_SENTENCE_TYPE`  
    Type of embedding model to use for Qdrant: `local` (local model) or `hf` (Hugging Face automatic download). If `local`, also set `VECTORDB_SENTENCE_PATH`; if `hf`, set `VECTORDB_SENTENCE_MODEL`.

- `VECTORDB_SENTENCE_MODEL`  
    Name of the embedding model (e.g. `BAAI/bge-small-en-v1.5` or others listed in the file). For `hf` it will be downloaded from Hugging Face; ignored for `local`.

- `LLM_MODEL_TYPE`  
    Type of LLM provider: supported values in the project e.g. `openai`, `ollama`, `vllm`. Determines the invocation method.

- `LLM_URL`  
    Endpoint of the LLM service (e.g. `http://localhost:11434` for Ollama or a custom API URL).

- `LLM_MODEL_NAME`  
    Name of the LLM model to use on the selected provider (e.g. `tinyllama`, `gpt-4.1-mini`, etc.).

- `MODEL_EMBEDDING`  
    Name of the embedding model for general use (e.g. `nomic-embed-text`, `text-embedding-3-small`). Must be compatible with the chosen provider.

- `NEO4J_USERNAME`  
    Username for connecting to Neo4j.

- `NEO4J_PASSWORD`  
    Password for Neo4j. Secret: do not commit.

- `NEO4J_AUTH`  
    Authentication string for Neo4j, typically in the format `username/password`. Some clients require this combined form.

- `REDIS_URL`  
    Redis connection URL, e.g. `redis://host:port`. May include credentials if needed (be cautious with security).

- `REDIS_HOST`  
    Redis host (used if `REDIS_URL` is not used).

- `REDIS_PORT`  
    Redis port (e.g. `6379`).

- `REDIS_DB`  
    Redis database index to use (integer).

- `APP_VERSION`  
    Application/image version (semver or free-form string) used for tracking/telemetry.

- `A2A_CLIENT`  
    URL of the agent-to-agent (A2A) client used for internal agent communications, e.g. `http://kgrag_agent:8010`.

Security and operational notes:
- Do not place keys and secrets in public repositories. Use a secret manager or an .env file excluded from VCS.  
- Some variables (embedding/LLM models) must be compatible with the local runtime or remote services configured; check the providers' documentation if you encounter loading errors.  
- If you use `VECTORDB_SENTENCE_TYPE=local`, set the local model path via the dedicated variable (not included in the example file).  
- Ensure `NEO4J_AUTH` matches the actual credentials used by the Neo4j container and that the host/container ports in the compose file are correct.  
- For Redis in containerized environments prefer the service host on the overlay network (e.g. `redis://redis:6379`) rather than `localhost`.  
- Change access defaults (e.g. Grafana anonymous admin) before exposing to production.  
- Always rotate keys that have been leaked or accidentally published.

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

