# Avito Helper

A toolkit for interacting with Avito API.

## Requirements
- Docker & docker-compose
- PostgreSQL

## Environment Variables
Create `.env` file (see `.env.example`). Required variables:

```
DATABASE_URL=postgresql+asyncpg://avito:avito@db:5432/avito
AVITO_CLIENT_ID=your_client_id
AVITO_CLIENT_SECRET=your_client_secret
AVITO_REFRESH_TOKEN=your_refresh_token
COMPETITOR_ITEM_IDS=1,2,3
```

## Usage

### Build and run
```
docker-compose build
docker-compose up
```

### CLI
Run commands inside the container or locally via Typer:
```
poetry run python -m avito_helper.app.cli --help
```
