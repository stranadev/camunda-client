import asyncio
import contextlib
from collections.abc import AsyncIterator, Sequence
from datetime import timedelta
from types import TracebackType
from typing import TYPE_CHECKING
from camunda_client.exceptions import CamundaClientError
from stamina import retry

from camunda_client.clients.external_task.schemas.response import ExternalTaskSchema

if TYPE_CHECKING:
    from camunda_client.clients import ExternalTaskClient

from .context import ExternalTaskContext
from .dto import ExternalTaskDTO
from .topic_consumer import TopicConsumer
from camunda_client._logger import logger


class ExternalTaskWorker:
    def __init__(
        self,
        client: "ExternalTaskClient",
        pull_interval: timedelta,
        business_key: str | None = None,
    ) -> None:
        self._consumers: dict[str, TopicConsumer] = {}
        self._pull_interval = pull_interval
        self._client = client
        self._business_key = business_key

        self._tg = asyncio.TaskGroup()
        self._closing = asyncio.Event()
        self._is_current_tasks_empty = asyncio.Event()
        self._is_current_tasks_empty.set()

        self._current_tasks: set[str] = set()

    async def __aenter__(self) -> None:
        await self._tg.__aenter__()
        self._tg.create_task(self._pull_tasks())

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._closing.set()
        await self._tg.__aexit__(exc_type, exc_val, exc_tb)

    async def _pull_tasks(self) -> None:
        while True:
            if self._consumers:
                tasks = await self._get_tasks()
                self._current_tasks = {item.id for item in tasks}

                for task in tasks:
                    logger.info('Got task with id "%s"', task.id)
                    consumer = self._consumers[task.topic_name]
                    ctx = ExternalTaskContext(
                        client=self._client,
                        task=ExternalTaskDTO.model_validate(task),
                        exit_hook=self._on_task_exit,
                    )
                    consumer.add_task(ctx)
                    self._is_current_tasks_empty.clear()

            await self._wait()

            if self._closing.is_set():
                return

    def _on_task_exit(self, task_id: str) -> None:
        self._current_tasks.remove(task_id)

        if not self._current_tasks:
            self._is_current_tasks_empty.set()

    @retry(on=CamundaClientError, attempts=3)
    async def _get_tasks(self) -> Sequence[ExternalTaskSchema]:
        return await self._client.fetch_and_lock(
            topic_names=list(self._consumers),
            business_key=self._business_key,
        )

    async def _wait(self) -> None:
        await self._is_current_tasks_empty.wait()

        _, pending = await asyncio.wait(
            [
                asyncio.create_task(
                    asyncio.sleep(self._pull_interval.total_seconds()),
                ),
                asyncio.create_task(self._closing.wait()),
            ],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

    @contextlib.asynccontextmanager
    async def subscribe(
        self,
        topic: str,
    ) -> AsyncIterator[AsyncIterator[ExternalTaskContext]]:
        topic_consumer = TopicConsumer(closing=self._closing)

        if topic in self._consumers:
            raise ValueError

        self._consumers[topic] = topic_consumer

        yield topic_consumer

        del self._consumers[topic]
