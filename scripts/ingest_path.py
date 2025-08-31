import asyncio
import os
import sys

# Ensure project root is on sys.path BEFORE imports from project
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import settings  # noqa: E402 (import after sys.path manipulation)

# Select kgrag impl based on env (same logic as server.py)
if settings.LLM_MODEL_TYPE == "ollama":
    from kgrag_ollama import kgrag_ollama as kgrag
elif settings.LLM_MODEL_TYPE == "openai":
    from kgrag_openai import kgrag_openai as kgrag
else:
    raise RuntimeError(
        f"Unsupported LLM_MODEL_TYPE: {settings.LLM_MODEL_TYPE!r}"
    )


async def run(path: str):
    if not os.path.exists(path):
        print(f"ERROR: file not found: {path}")
        sys.exit(1)

    async for d in kgrag.process_documents(path=path, force=True):
        print(d)
    print(f"DONE: {path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python scripts/ingest_path.py "
            "/absolute/path/to/file.pdf"
        )
        sys.exit(2)
    target = sys.argv[1]
    asyncio.run(run(target))
