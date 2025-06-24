FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY pyproject.toml poetry.lock* /app/
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY . /app

CMD ["python", "-m", "avito_helper.app.cli", "run-scheduler"]
