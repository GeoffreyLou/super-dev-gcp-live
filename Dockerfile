FROM python:3.11-slim

WORKDIR /app
COPY . /app/

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN pip install uv
RUN uv venv && uv sync
ENV PATH="app/.venv/bin:$PATH"

ENTRYPOINT ["uv", "run", "src/main.py"]