# Development

## 🛠️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/gzileni/kgrag_mcp_server.git
cd kgrag_mcp_server
```

### 2. Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔧 Environment Variables

Before starting development, copy each `env.xxxx.template` file to its corresponding `.env.xxxx` file. For example:

```bash
cp env.development.template .env.development
cp env.production.template .env.production
cp env.ollama.production.template .env.ollama.production
cp env.ollama.development.template .env.development.production
cp env.openai.development.template .env.openai.development
cp env.openai.production.template .env.openai.production
cp env.vllm.production.template .env.vllm.production
cp env.vllm.development.template .env.vllm.development
cp env.template .env 
```

Edit the copied `.env.xxxx` files as needed for your environment.

Example organization for multiple environments:

```bash
.env.development
.env.production
.env.ollama.production
.env.development.production
.env.openai.development
.env.openai.production
.env.vllm.production
.env.vllm.development
.env 
```

### 🌍 General

| Variable               | Default              | Description                                                                 |
| ---------------------- | -------------------- | --------------------------------------------------------------------------- |
| `APP_ENV`              | `development`        | Execution environment (`development`, `staging`, `production`, `test`).     |
| `COLLECTION_NAME`      | `kgrag_data`         | Name of the collection for data ingestion.                                  |

### ☁️ AWS S3

| Variable                | Default          | Description                              |
| ----------------------- | ---------------- | ---------------------------------------- |
| `AWS_ACCESS_KEY_ID`     | **required**     | AWS access key for S3 access.            |
| `AWS_SECRET_ACCESS_KEY` | **required**     | AWS secret key for S3 access.            |
| `AWS_BUCKET_NAME`       | **required**     | Name of the S3 bucket.                   |
| `AWS_REGION`            | **required**     | AWS region.                              |

### 🗄️ Neo4j

| Variable         | Default                   | Description                                         |
| ---------------- | ------------------------- | --------------------------------------------------- |
| `NEO4J_URL`      | `neo4j://localhost:47687` | Neo4j connection URL.                               |
| `NEO4J_USERNAME` | `neo4j`                   | Username for Neo4j.                                 |
| `NEO4J_PASSWORD` | `n304j2025`               | Password for Neo4j.                                 |
| `NEO4J_DB_NAME`  | *(empty)*                 | Neo4j database name (if different from default).    |

### 🔄 Redis

| Variable     | Default                  | Description                |
| ------------ | ------------------------ | -------------------------- |
| `REDIS_URL`  | `redis://localhost:6379` | Full URL for Redis.        |
| `REDIS_HOST` | `localhost`              | Redis host.                |
| `REDIS_PORT` | `6379`                   | Redis port.                |
| `REDIS_DB`   | `4`                      | Redis database number.     |

### 🔍 Qdrant

| Variable     | Default                 | Description                |
| ------------ | ----------------------- | -------------------------- |
| `QDRANT_URL` | `http://localhost:6333` | Qdrant instance URL.       |


### 📊 Loki

| Variable   | Default                                  | Description                |
| ---------- | ---------------------------------------- | -------------------------- |
| `LOKI_URL` | `http://localhost:3100/loki/api/v1/push` | Loki push URL.             |


### 🤖 LLM (Large Language Model)

| Variable            | Default                  | Description                                         |
| ------------------- | ------------------------ | --------------------------------------------------- |
| `LLM_MODEL_TYPE`    | `openai`                 | Model type (`openai`, `azure`, `local`, etc.).      |
| `LLM_MODEL_NAME`    | `gpt-4.1-mini`           | Name of the LLM model to use.                       |
| `LLM_EMBEDDING_URL` | *(empty)*                | Custom embedding endpoint.                          |
| `MODEL_EMBEDDING`   | `text-embedding-3-small` | Model for embeddings.                               |
| `LLM_URL`           | *(empty)*                | LLM API endpoint.                                   |


### 🧠 Vector DB

| Variable                  | Default                  | Description                                 |
| ------------------------- | ------------------------ | ------------------------------------------- |
| `VECTORDB_SENTENCE_MODEL` | `BAAI/bge-small-en-v1.5` | Embedding model for vectors.                |
| `VECTORDB_SENTENCE_TYPE`  | `hf`                     | Model type (`hf`, `local`).                 |
| `VECTORDB_SENTENCE_PATH`  | *(empty)*                | Local path for vector model.

---

## ⚙️ Docker

This project uses **Docker Compose** to run the **KGrag Agent** stack.
The **Makefile** provides quick commands to start, stop, and restart services.

### 📦 Requirements

* [Docker](https://docs.docker.com/get-docker/) ≥ 20.x
* [Docker Compose](https://docs.docker.com/compose/) ≥ 2.x
* [Make](https://www.gnu.org/software/make/)

### 🚀 Available Commands

#### ▶️ Start the stack

Start all services in **detached** mode (`-d`):

```bash
make run
```

Internally runs:

```bash
docker-compose -p kgrag-agent up -d
```

#### ⏹️ Stop the stack

Stops and removes containers defined in `docker-compose.yml`:

```bash
make stop
```

Internally runs:

```bash
docker-compose down
```

#### 🔄 Restart the stack

Stops and restarts services:

```bash
make restart
```

Equivalent to:

```bash
make stop && make run
```

### 📜 Notes

* The stack uses the **Docker Compose project** named `kgrag-agent`.
* You can customize services by editing the `docker-compose.yml` file.
* To view logs in real time:

```bash
docker-compose -p kgrag-agent logs -f
```



