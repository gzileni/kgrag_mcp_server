import os
from mcp.server.fastmcp import FastMCP, Context
from memory_agent.kgrag import (
    parser_prompt,
    query_prompt
)
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from typing import Optional
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
    name="extract_graph_data",
    description="Extract graph data from a document using the KGraph system."
)
async def extract_graph_data(
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
    title="KGrag Parser",
    name="parser",
    description="Parse a document using the KGraph system.",
)
async def parser(
    text: str,
    ctx: Context,
    prompt_user: Optional[str] = None
):
    """
    Parse a document using the KGraph system.
    Args:
        text (str): Text to be parsed.
        ctx (Context): Context for logging and reporting progress.
    Returns:
        str: Parsed relationships in JSON format.
    """
    if not isinstance(text, str):
        return "text must be a string."
    if not text.strip():
        return "text cannot be an empty string."

    components = await kgrag.llm_parser(
        prompt_text=text,
        prompt_user=prompt_user
    )
    await ctx.info(f"Parsed Relationships: {components}")
    if isinstance(components, (str, dict, list)):
        return components
    return components.model_dump()


@mcp.tool(
    title="Query KGraph",
    name="query",
    description="Query the KGraph system with a specific query string."
)
async def query(
    q: str,
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

    await ctx.info(f"Querying KGraph: {q}")
    return await kgrag.query(q)


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


@mcp.prompt(title="Parser Text Prompt")
def parser_text_prompt(text: Optional[str] = None) -> str:
    """
    Generate a prompt for extracting relationships from text.
    Args:
        text (str): The input text to extract relationships from.
    Returns:
        str: The formatted prompt for the relationship extractor.
    """
    return parser_prompt(text)


@mcp.prompt(title="Agent Query Prompt")
def agent_query_prompt(
    nodes_str: str,
    edges_str: str,
    user_query: str
) -> str:
    """
    Generate a prompt for the agent to answer a user query
    using the knowledge graph.
    Args:
        nodes_str (str): String representation of nodes in the graph.
        edges_str (str): String representation of edges in the graph.
        user_query (str): The user's query to be answered.
    Returns:
        str: The formatted prompt for the agent.
    """
    return query_prompt(
        nodes_str=nodes_str,
        edges_str=edges_str,
        user_query=user_query
    )


# Mount the SSE server to the existing ASGI server
app = Starlette(
    routes=[
        Route("/healthz", endpoint=health),
        Mount("/", app=mcp.sse_app()),
    ]
)
