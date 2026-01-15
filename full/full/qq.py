import asyncio
from collections.abc import AsyncGenerator

from quasiqueue import QuasiQueue

from .settings import settings
from full.services.cache import configure_caches


async def writer(desired: int) -> AsyncGenerator[int, None]:
    """Feeds data to the Queue when it is low."""
    for x in range(0, desired):
        yield x


async def reader(identifier: int | str) -> None:
    """Receives individual items from the queue.

    Args:
        identifier (int | str): Comes from the output of the Writer function
    """
    print(f"{identifier}")


runner = QuasiQueue(
    settings.project_name,
    reader=reader,  # type: ignore[arg-type]
    writer=writer,  # type: ignore[arg-type]
    settings=settings,
)

if __name__ == "__main__":
    # Initialize caches before running QuasiQueue
    configure_caches()
    asyncio.run(runner.main())
