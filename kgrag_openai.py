from memory_agent.kgrag.openai import KGragOpenAI
from kgrag_config import (
    model_config,
    neo4j_auth,
    redis_config,
    model_embedding_vs_config,
    collection_config,
    model_embedding_config,
    aws_config,
    qdrant_config
)
from config import settings

kgrag_openai = KGragOpenAI(
    path_type="fs",
    path_download=settings.PATH_DOWNLOAD,
    format_file="pdf",
    neo4j_auth=neo4j_auth,
    qdrant_config=qdrant_config,
    host_persistence_config=redis_config,
    aws_config=aws_config,
    model_embedding_config=model_embedding_config,
    model_embedding_vs_config=model_embedding_vs_config,
    collection_config=collection_config,
    llm_config=model_config
)
