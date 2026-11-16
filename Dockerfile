FROM python:3.14-slim

# uv dari image resmi, lalu dependensi dipasang persis sesuai uv.lock
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_SYNC=1 \
    UV_CACHE_DIR=/tmp/uv-cache \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

COPY . .

# Rahasia tidak ada di image: nilai ini hanya dipakai sesaat saat build.
RUN SECRET_KEY=hanya-untuk-build DEBUG=False python manage.py collectstatic --noinput

# Jalankan sebagai user non-root
RUN useradd --create-home --uid 1000 app \
    && mkdir -p /app/media \
    && chown -R app:app /app/media /app/staticfiles \
    && chmod +x /app/docker-entrypoint.sh
USER app

EXPOSE 8000

# Mendengarkan port dari variabel PORT (default 8000) agar image sama bisa dipakai di Render/Railway.
# docker-entrypoint.sh menjalankan migrate lalu Gunicorn.
ENTRYPOINT ["./docker-entrypoint.sh"]
