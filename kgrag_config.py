from qdrant_client.http.models import Distance
from typing import Any
from config import settings

model_config = {
    "model": settings.LLM_MODEL_NAME,
    "model_provider": settings.LLM_MODEL_TYPE,
    "api_key": settings.API_KEY,
    "base_url": settings.LLM_URL,
    "temperature": settings.TEMPERATURE,
}

neo4j_auth: dict[str, Any] = {
    "url": settings.NEO4J_URL,
    "username": settings.NEO4J_USERNAME,
    "password": settings.NEO4J_PASSWORD,
    "database": settings.NEO4J_DB_NAME,
}

redis_config = {
    "host": settings.REDIS_HOST,
    "port": settings.REDIS_PORT,
    "db": settings.REDIS_DB,
}

model_embedding_vs_config = {
    "path": None,
    "type": settings.VECTORDB_SENTENCE_TYPE,
    "name": settings.VECTORDB_SENTENCE_MODEL
}

collection_config = {
    "collection_name": settings.COLLECTION_NAME,
    "vectors_config": {
        "size": 1536,
        # COSINE = "Cosine"
        # EUCLID = "Euclid"
        # DOT = "Dot"
        # MANHATTAN = "Manhattan"
        "distance": Distance.COSINE
    }
}

qdrant_config = {
    "url": settings.QDRANT_URL,
}

model_embedding_config = {
    "name": settings.MODEL_EMBEDDING,
    "url": settings.LLM_EMBEDDING_URL,
}

aws_config = {
    "access_key_id": settings.AWS_ACCESS_KEY_ID,
    "secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
    "bucket": settings.AWS_BUCKET_NAME,
    "region": settings.AWS_REGION
}
