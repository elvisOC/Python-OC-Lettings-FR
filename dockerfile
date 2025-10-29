# -------- Stage 1 : Build --------
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip wheel -r requirements.txt --wheel-dir=/wheels

COPY . /app

# -------- Stage 2 : Runtime --------
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=oc_lettings_site.settings \
    SECRET_KEY="" \
    DEBUG=0 \
    ALLOWED_HOSTS=python-oc-lettings-fr-y4n6.onrender.com

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY --from=builder /app /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENV PORT=8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "oc_lettings_site.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--log-level", "info"]
