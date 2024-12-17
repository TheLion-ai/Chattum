FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /frontend
COPY . /frontend

RUN uv sync --frozen

CMD ["uv", "run", "streamlit", "run", "🤖_bots.py"]
