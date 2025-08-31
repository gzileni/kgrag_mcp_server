ARG BASE_IMAGE_CPU=ghcr.io/gzileni/kgrag-store:cpu
ARG BASE_IMAGE_GPU=ghcr.io/gzileni/kgrag-store:gpu
ARG PLATFORM=cpu

# === Stage per CPU ===
FROM ${BASE_IMAGE_CPU} AS base_cpu

# === Stage per GPU ===
FROM ${BASE_IMAGE_GPU} AS base_gpu

# === Seleziona lo stage finale ===
ARG PLATFORM
FROM base_${PLATFORM} AS final

# QDrant port
EXPOSE 6333 6334

ENV \
  USER_AGENT="KGrag Agent" \
  APP_VERSION="1.0.0" \
  APP_ENV="production" 

WORKDIR /app

# Crea un virtualenv
RUN python3 -m venv /app/venv

# Copia requirements prima per sfruttare la cache
COPY requirements.txt .

# Attiva il venv con source (POSIX '.') e installa i pacchetti
RUN . /app/venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt uv uvicorn

# Metti il venv nel PATH per i layer successivi
ENV PATH="/app/venv/bin:$PATH"

# Copia i sorgenti
COPY *.py .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

RUN cat <<'SUPERVISOR_CONF' >> /etc/supervisor/conf.d/supervisord.conf
[program:app]
command=/app/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8000
directory=/app
autostart=true
autorestart=true
stdout_logfile=/var/log/app.out.log
stderr_logfile=/var/log/app.err.log
startsecs=5
SUPERVISOR_CONF

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]