import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from full.models.base import Base
from full.services.db import get_session_depends, test_data
from fastapi.testclient import TestClient
from full.www import app


@pytest_asyncio.fixture
async def db_session_maker(tmpdir):
    """Creates a test database engine, complete with fake data."""
    test_database_url = f"sqlite+aiosqlite:///{tmpdir}/test_database.db"  # Use SQLite for testing; adjust as needed
    engine = create_async_engine(test_database_url, future=True, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_maker() as session:
        await test_data(session)

    yield async_session_maker

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_session_maker):
    async with db_session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def fastapi_client(db_session_maker):
    """Fixture to create a FastAPI test client."""
    client = TestClient(app)

    async def get_session_depends_override():
        async with db_session_maker() as session:
            yield session

    app.dependency_overrides[get_session_depends] = get_session_depends_override
    yield client
