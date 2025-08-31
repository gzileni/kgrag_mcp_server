from memory_agent.openai import KGragOpenAI
from config import settings

kgrag_openai = KGragOpenAI(
    path_type="fs",
    path_download=settings.PATH_DOWNLOAD,
    format_file="pdf",
    collection_name=settings.COLLECTION_NAME,
    model_name=settings.LLM_MODEL_NAME,
    model_embedding_name=settings.MODEL_EMBEDDING,
    model_embedding_url=settings.LLM_URL,
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
    redis_db=settings.REDIS_DB,
    llm_api_key=settings.OPENAI_API_KEY
)
