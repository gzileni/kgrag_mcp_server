# KGrag MCP Server

**KGrag MCP Server** is a server that implements the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for managing, ingesting, and querying structured and unstructured data.
It is designed for easy integration with graph databases (Neo4j), AWS S3 storage, Redis cache, vector search engines (Qdrant), and advanced language models (LLM).  
The project provides a scalable, containerized infrastructure via Docker Compose to orchestrate data pipelines, semantic enrichment, and analysis through advanced queries.  
Ideal for knowledge graph, AI, and information flow automation applications.

## Example: Ingestion and Query with GitHub Copilot in VSCode (Agent Mode)

You can use GitHub Copilot in VSCode to interactively ingest documents into the MCP Server using an agent-based workflow and a configuration file.

**Step-by-step:**

1. **Open VSCode** and ensure GitHub Copilot is enabled.
2. **Create an `mcp.json` configuration file** in your project directory:

```json
{
	"servers": {
		"kgrag-server": {
			"url": "http://localhost:8000/sse",
			"type": "sse"
		}
	},
	"inputs": []
}
```

3. **Let Copilot suggest ingestion code and improvements** such as error handling or batch processing, using the configuration from `mcp.json`.

This workflow enables rapid prototyping and automation of ingestion tasks with Copilot's agent capabilities and a configurable server endpoint.

![kgrag](./kgrag-mcp-server.gif)

---

## Dependencies

- [`kgrag-store`](https://github.com/gzileni/kgrag-store): Core data storage and graph management library.
- [`memory-agent`](https://github.com/gzileni/memory-agent): A Python library for advanced memory management in AI agent applications

---

## [Development](DEV.md)

---

## **Tools**

### `query`

Queries the **Knowledge Graph** to obtain answers based on stored documents and relationships.

**Parameters**:

* `query` (`str`) → Question to ask the graph.

### `ingestion`

Ingests a document from the file system into the graph.

**Parameters**:

* `path` (`str`) → Path to the file to ingest.


###  `extract_graph_data`

Extract graph data from a document using the KGraph system

**Parameters**:

* `raw_data` (`str`) → Raw data to process.

###  `parser`

Parse a document using the KGraph system.

**Parameters**:

* `text` (`str`) → Text to be parsed.

---

## **Prompts**

### 📜 `parser_text_prompt`

Generates the **prompt** to extract relationships from text.

```python
@mcp.prompt(title="Parser Text Prompt")
def parser_text_prompt(text: Optional[str] = None) -> str:
```

### 🤖 `agent_query_prompt`

Generates the **prompt** to answer graph-based queries.

```python
@mcp.prompt(title="Agent Query Prompt")
```

Uses the `AGENT_PROMPT` constant and formats data from:

* `nodes_str` → list of nodes
* `edges_str` → list of relationships
* `user_query` → user question

---

## [Docker](./docker/README.md)


