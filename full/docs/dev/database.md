# Database

This project uses [SQLAlchemy](https://www.sqlalchemy.org/) and [Alembic](https://alembic.sqlalchemy.org/en/latest/) to build migrations.

## Database API

This project uses SQLAlchemy 1.4 and 2.0 APIs. It exposes the Async Engine and AsyncSessions.

## Engines

This project is geared towards Postgres and SQLite.

## Models

Models exists in the `full/models` directory.


## Migrations

Migrations are created with Alembic. It will automatically find all models in the `full/models` directory.

Migrations can be using `make`. This method uses SQLite.

```bash
make create_migration MESSAGE="migration description"
```

## FastAPI Integration

The function `full.db:get_session_depends` is designed to work with the [FastAPI Dependency system](https://fastapi.tiangolo.com/tutorial/dependencies/), and can be passed directly to [Depends](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
