from kgrag_store import KGragRetriever
from config import settings


model_embedding_url: str | None = None
llm_model_url: str | None = None
if settings.LLM_MODEL_TYPE == "ollama" and settings.LLM_URL is not None:
    model_embedding_url = f"{settings.LLM_URL}/api/embeddings"
    llm_model_url = settings.LLM_URL

kgrag = KGragRetriever(
    path_type="fs",
    path_download=settings.PATH_DOWNLOAD,
    format_file="pdf",
    collection_name=settings.COLLECTION_NAME,
    llm_model=settings.LLM_MODEL_NAME,
    llm_type=settings.LLM_MODEL_TYPE,
    llm_model_url=llm_model_url,
    model_embedding_type=settings.LLM_MODEL_TYPE,
    model_embedding_name=settings.MODEL_EMBEDDING,
    model_embedding_url=model_embedding_url,
    model_embedding_vs_name=settings.VECTORDB_SENTENCE_MODEL,
    model_embedding_vs_type=settings.VECTORDB_SENTENCE_TYPE,
    model_embedding_vs_path=settings.VECTORDB_SENTENCE_PATH,
    neo4j_url=settings.NEO4J_URL,
    neo4j_username=settings.NEO4J_USERNAME,
    neo4j_password=settings.NEO4J_PASSWORD,
    neo4j_db_name=settings.NEO4J_DB_NAME,
    qdrant_url=settings.QDRANT_URL,
    redis_host=settings.REDIS_HOST,
    redis_port=settings.REDIS_PORT,
    redis_db=settings.REDIS_DB
)
