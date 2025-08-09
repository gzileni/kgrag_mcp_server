import os
from mcp.server.fastmcp import FastMCP, Context
from kgrag_store import (
    parser_prompt,
    query_prompt,
    GraphComponents
)
from starlette.applications import Starlette
from starlette.routing import Mount
from kgrag import kgrag
from typing import Optional

# Initialize FastMCP server
mcp = FastMCP("KGraph")


@mcp.tool(
    title="Extract Graph Data",
    name="extract_graph_data",
    description="Extract graph data from a document using the KGraph system."
)
async def extract_graph_data(
    raw_data: str,
    ctx: Context
) -> tuple[dict[str, str], list[dict[str, str]]]:
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
    return nodes, relationships


@mcp.tool(
    title="KGrag Parser",
    name="parser",
    description="Parse a document using the KGraph system.",
)
async def parser(
    text: str,
    ctx: Context,
    prompt_user: Optional[str] = None
) -> GraphComponents | str:
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
    return components


@mcp.tool(
    title="Query KGraph",
    name="query",
    description="Query the KGraph system with a specific query string."
)
async def query(
    query: str,
    ctx: Context
):
    """
    Query the KGraph system with a specific query string.
    Args:
        query (str): Query for the document to be ingested.
    """
    if not isinstance(query, str):
        return "query must be a string."
    if not query.strip():
        return "query cannot be an empty string."

    return await kgrag.query(query)


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
        Mount('/', app=mcp.sse_app()),
    ]
)
