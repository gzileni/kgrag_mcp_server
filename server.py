import os
from mcp.server.fastmcp import FastMCP, Context
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.responses import (
    PlainTextResponse,
)
from starlette.routing import Route
from config import settings

# Initialize FastMCP server
mcp = FastMCP("KGraph MCP Server")

# Register KGrag instance based on LLM model type
# Import into a temporary name and then assign
# to `kgrag` so the variable is always defined,
# and raise a clear error for unsupported configuration.
_kgrag = None

if settings.LLM_MODEL_TYPE == "ollama":
    from kgrag_ollama import kgrag_ollama as _kgrag
elif settings.LLM_MODEL_TYPE == "openai":
    from kgrag_openai import kgrag_openai as _kgrag
else:
    raise RuntimeError(
        "Unsupported LLM_MODEL_TYPE: "
        + f"{settings.LLM_MODEL_TYPE!r}. Expected 'ollama' or 'openai'."
    )

kgrag = _kgrag


async def health(_):
    return PlainTextResponse("ok")


@mcp.tool(
    title="Extract Graph Data",
    name="extract",
    description="Extract graph data from a document using the KGraph system."
)
async def extract(
    raw_data: str,
    ctx: Context
) -> dict:
    """
    Extract graph data from a document using the KGraph system.
    Args:
        raw_data (str): Raw data to be processed.
        ctx (Context): Context for logging and reporting progress.
    Returns:
        tuple: A tuple containing a dictionary of nodes and a list of edges.
    """
    if not isinstance(raw_data, str):
        return {}, []

    nodes, relationships = await kgrag.extract_graph_components(raw_data)
    await ctx.info(f"Extracted Graph Data: {nodes}, {relationships}")
    return {"nodes": nodes, "relationships": relationships}


@mcp.tool(
    title="Query KGraph",
    name="query",
    description="Query the KGraph system with a specific query string."
)
async def query(
    prompt: str,
    ctx: Context
):
    """
    Query the KGraph system with a specific query string.
    Args:
        query (str): Query for the document to be ingested.
    """
    if not isinstance(q, str):
        return "query must be a string."
    if not q.strip():
        return "query cannot be an empty string."

    await ctx.info(f"Querying KGraph: {prompt}")
    return await kgrag.query(prompt)


@mcp.tool(
    title="Ingest",
    name="ingestion",
    description="Ingest a path of file into the KGraph system."
)
async def ingestion(
    path: str,
    ctx: Context
):
    """
    Ingest a document into the KGraph system.
    Args:
        args (dict): Arguments containing the path to the document.
            - path (str): Path to the document file to be ingested.
        ctx (Context): Context for logging and reporting progress.
    Returns:
        str: Confirmation message indicating successful ingestion.
    """

    if not isinstance(path, str):
        return "path_file must be a string."
    if not path.strip():
        return "path_file cannot be an empty string."
    if not os.path.exists(path):
        return f"File {path} does not exist."

    async for d in kgrag.process_documents(
        path=path,
        force=True
    ):
        if d == "ERROR":
            return f"Error processing document {path}."
        await ctx.info(f"{d}")
    return f"Document {path} ingested successfully."

# Mount the SSE server to the existing ASGI server
app = Starlette(
    routes=[
        Route(
            "/healthz",
            endpoint=health
        ),
        Mount(
            "/",
            app=mcp.sse_app()
        ),
    ]
)
