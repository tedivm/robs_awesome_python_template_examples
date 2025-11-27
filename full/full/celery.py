from typing import Any

from celery import Celery  # type: ignore[import-untyped]

celery = Celery("full")


@celery.task
def hello_world() -> None:
    print("Hello World!")


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender: Any, **kwargs: Any) -> None:
    print("Enabling Test Task")
    sender.add_periodic_task(15.0, hello_world.s(), name="Test Task")
