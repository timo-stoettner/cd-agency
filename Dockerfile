FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY runtime/ runtime/
COPY tools/ tools/
COPY content-design/ content-design/
COPY workflows/ workflows/
COPY presets/ presets/

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["cd-agency"]
CMD ["--help"]
