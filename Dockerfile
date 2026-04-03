FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY tests /app/tests

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .[dev]

CMD ["pytest"]
