import dataclasses
import logging
from functools import wraps
from typing import Callable
from uuid import uuid4

logger = logging.getLogger("task_worker")

TASK_REGISTRY = {}


@dataclasses.dataclass
class Task:
    task_func: callable
    queue_key: str
    description: str = None
    task_module: str = None

    def __post_init__(self):
        self.task_module = self.task_func.__module__
        func = self.task_func
        while hasattr(func, "__wrapped__"):
            func = func.__wrapped__
            self.task_module = func.__module__
        self.name = func.__name__

    def register(self):
        if self.queue_key in TASK_REGISTRY:
            raise NameError(f"Task {self.queue_key} already registered.")
        TASK_REGISTRY[self.queue_key] = self

    def __str__(self):
        return f"Task: {self.name} | Queue Key: {self.queue_key} | Task func: {self.task_func} "


def task(queue_key: str, description: str = None, skip_logging: bool = False):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            uuid = uuid4()
            try:
                if not skip_logging:
                    logger.info(f"[{uuid}]Task {func.__name__} started.")
                await func(*args, **kwargs)
                if not skip_logging:
                    logger.info(f"{uuid}Task {func.__name__} finished.")

            except Exception as e:
                logger.error(f"{uuid}Task {func.__name__} failed.")
                raise e

        wrapper._original = func
        task_obj = Task(wrapper, queue_key, description)
        task_obj.register()

        return wrapper

    return decorator
