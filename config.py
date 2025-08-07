"""Application configuration management.

This module handles environment-specific configuration loading, parsing,
and management
for the application. It includes environment detection, .env file loading, and
configuration value parsing.
"""

import os
from enum import Enum
from dotenv import load_dotenv
from typing import Literal
from log import logger

TypeStorage = Literal["s3", "local"]


# Define environment types
class Environment(str, Enum):
    """Application environment types.

    Defines the possible environments the application can run in:
    development, staging, production, and test.
    """

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


def get_path_fs(prefix: str) -> str:
    """
    Get the local filesystem path for the given object name.

    Args:
        object_name (str): The name of the object.

    Returns:
        str: The local filesystem path.
    """

    prefix = f".{prefix}/"
    if not os.path.exists(prefix):
        os.makedirs(prefix)

    path_root = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
    path_fs = os.path.join(path_root, prefix)
    if not os.path.exists(path_fs):
        os.makedirs(path_fs)
    return path_fs


# Determine environment
def get_environment() -> Environment:
    """
    Get the current environment.

    Returns:
        Environment: The current environment
        (development, staging, production, or test)
    """
    match os.getenv("APP_ENV", "production").lower():
        case "production" | "prod":
            return Environment.PRODUCTION
        case "staging" | "stage":
            return Environment.STAGING
        case "test":
            return Environment.TEST
        case _:
            return Environment.DEVELOPMENT


# Load appropriate .env file based on environment
def load_env_file():
    """Load environment-specific .env file."""
    env = get_environment()
    print(f"Loading environment: {env}")
    path_env = os.path.dirname(os.path.abspath(__file__))

    # Define env files in priority order
    env_files = [
        os.path.join(path_env, f".env.{env.value}.local"),
        os.path.join(path_env, f".env.{env.value}"),
        os.path.join(path_env, ".env.local"),
        os.path.join(path_env, ".env"),
    ]

    # Load the first env file that exists
    for env_file in env_files:
        if os.path.exists(env_file):
            load_dotenv(dotenv_path=env_file)
            print(f"Loaded environment from {env_file}")
            return env_file

    # Fall back to default if no env file found
    return None


def load_env_llm(model: str):
    """Load environment variables for LLM configuration."""
    env = get_environment()
    env_file_llm = f".env.{model}.{env.value}"
    print(f"Loading LLM environment: {env_file_llm}")

    # leggi la cartella corrente del file
    path_env = os.path.dirname(os.path.abspath(__file__))
    env_llm = os.path.join(path_env, env_file_llm)
    if os.path.exists(env_llm):
        load_dotenv(dotenv_path=env_llm)
        print(f"Loaded LLM environment from {env_llm}")


ENV_FILE = load_env_file()


def get_path_ingestion(collection_name: str) -> str:
    """
    Get the path for data ingestion.
    Returns:
        str: The path for data ingestion.
    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(current_path, "tmp")
    if not os.path.exists(p):
        os.makedirs(p)
    p = os.path.join(p, collection_name)
    if not os.path.exists(p):
        os.makedirs(p)
    return p


# Parse list values from environment variables
def parse_list_from_env(env_key, default=None):
    """Parse a comma-separated list from an environment variable."""
    value = os.getenv(env_key)
    if not value:
        return default or []

    # Remove quotes if they exist
    value = value.strip("\"'")
    # Handle single value case
    if "," not in value:
        return [value]
    # Split comma-separated values
    return [item.strip() for item in value.split(",") if item.strip()]


# Parse dict of lists from environment variables with prefix
def parse_dict_of_lists_from_env(prefix, default_dict=None):
    """
    Parse dictionary of lists from environment variables
    with a common prefix.
    """
    result = default_dict or {}

    # Look for all env vars with the given prefix
    for key, value in os.environ.items():
        if key.startswith(prefix):
            endpoint = key[len(prefix):].lower()  # Extract endpoint name
            # Parse the values for this endpoint
            if value:
                value = value.strip("\"'")
                if "," in value:
                    result[endpoint] = [
                        item.strip()
                        for item in value.split(",")
                        if item.strip()
                    ]
                else:
                    result[endpoint] = [value]

    return result


class Settings:
    """Application settings without using pydantic."""

    def __init__(self):
        """Initialize application settings from environment variables.

        Loads and sets all configuration values from environment variables,
        with appropriate defaults for each setting. Also applies
        environment-specific overrides based on the current environment.
        """
        # Set the environment
        self.ENVIRONMENT = get_environment()
        self.APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

        self.AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        self.AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
        self.AWS_REGION = os.getenv('AWS_REGION')

        self.COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'kgrag_data')
        logger.info(f"Collection Name: {self.COLLECTION_NAME}")

        self.PATH_DOWNLOAD = get_path_ingestion(
            f"{self.COLLECTION_NAME}"
        )
        logger.info(f"Path Download: {self.PATH_DOWNLOAD}")

        # Neo4j settings
        self.NEO4J_URL = os.getenv('NEO4J_URL', 'neo4j://localhost:7687')
        self.NEO4J_USERNAME = os.getenv('NEO4J_USERNAME', 'neo4j')
        self.NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'n304j2025')
        self.NEO4J_DB_NAME = os.getenv('NEO4J_DB_NAME', None)
        logger.info(f"Neo4j URL: {self.NEO4J_URL}")
        logger.info(f"Neo4j Username: {self.NEO4J_USERNAME}")
        if self.NEO4J_DB_NAME:
            logger.info(f"Neo4j DB Name: {self.NEO4J_DB_NAME}")

        # Redis settings
        self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        self.REDIS_PORT = os.getenv("REDIS_PORT", 6379)
        self.REDIS_DB = os.getenv("REDIS_DB", 4)
        logger.info(f"Redis URL: {self.REDIS_URL}")
        logger.info(f"Redis Host: {self.REDIS_HOST}")
        logger.info(f"Redis Port: {self.REDIS_PORT}")
        logger.info(f"Redis DB: {self.REDIS_DB}")

        self.QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
        logger.info(f"Qdrant URL: {self.QDRANT_URL}")

        self.LOKI_URL = os.getenv(
            'LOKI_URL',
            'http://localhost:3100/loki/api/v1/push'
        )
        logger.info(f"Loki URL: {self.LOKI_URL}")

        self.LLM_MODEL_TYPE = os.getenv('LLM_MODEL_TYPE', 'openai')
        load_env_llm(self.LLM_MODEL_TYPE)
        logger.info(f"LLM Model Type: {self.LLM_MODEL_TYPE}")
        self.LLM_MODEL_NAME = os.getenv('LLM_MODEL_NAME', 'gpt-4.1-mini')
        logger.info(f"LLM Model Name: {self.LLM_MODEL_NAME}")
        self.LLM_EMBEDDING_URL = os.getenv(
            "LLM_EMBEDDING_URL",
            None
        )
        if self.LLM_EMBEDDING_URL:
            logger.info(f"LLM Embedding URL: {self.LLM_EMBEDDING_URL}")
        self.MODEL_EMBEDDING = os.getenv(
            "MODEL_EMBEDDING",
            "text-embedding-3-small"
        )
        logger.info(f"Model Embedding: {self.MODEL_EMBEDDING}")
        # LLM settings
        self.LLM_URL = os.getenv("LLM_URL", None)
        if self.LLM_URL:
            logger.info(f"LLM URL: {self.LLM_URL}")

        self.VECTORDB_SENTENCE_MODEL = os.getenv(
            "VECTORDB_SENTENCE_MODEL",
            "BAAI/bge-small-en-v1.5"
        )
        logger.info(f"VectorDB Sentence Model: {self.VECTORDB_SENTENCE_MODEL}")
        self.VECTORDB_SENTENCE_TYPE = os.getenv(
            "VECTORDB_SENTENCE_TYPE",
            "hf"
        )
        logger.info(f"VectorDB Sentence Type: {self.VECTORDB_SENTENCE_TYPE}")
        self.VECTORDB_SENTENCE_PATH = os.getenv("VECTORDB_SENTENCE_PATH", None)
        if self.VECTORDB_SENTENCE_PATH:
            logger.info(
                f"VectorDB Sentence Path: {self.VECTORDB_SENTENCE_PATH}"
            )

        # Apply environment-specific settings
        self.apply_environment_settings()

    def apply_environment_settings(self):
        """
        Apply environment-specific settings based
        on the current environment.
        """
        env_settings = {
            Environment.DEVELOPMENT: {
                "DEBUG": True,
                "LOG_LEVEL": "DEBUG",
                "LOG_FORMAT": "console"
            },
            Environment.STAGING: {
                "DEBUG": False,
                "LOG_LEVEL": "INFO"
            },
            Environment.PRODUCTION: {
                "DEBUG": False,
                "LOG_LEVEL": "WARNING"
            },
            Environment.TEST: {
                "DEBUG": True,
                "LOG_LEVEL": "DEBUG",
                "LOG_FORMAT": "console"
            },
        }

        # Get settings for current environment
        current_env_settings = env_settings.get(self.ENVIRONMENT, {})

        # Apply settings if not explicitly set in environment variables
        for key, value in current_env_settings.items():
            env_var_name = key.upper()
            # Only override if environment variable wasn't explicitly set
            if env_var_name not in os.environ:
                setattr(self, key, value)


# Create settings instance
settings = Settings()
