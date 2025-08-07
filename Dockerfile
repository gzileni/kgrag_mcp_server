FROM python:3.12-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt || true

COPY . .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
# ENTRYPOINT ["sh", "-c", "uvicorn main:app --host=$UVICORN_HOST --port=$UVICORN_PORT --log-level=$UVICORN_LOG_LEVEL --workers=$UVICORN_WORKERS"]
