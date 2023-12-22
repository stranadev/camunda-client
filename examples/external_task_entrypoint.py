import asyncio
import contextlib
from datetime import timedelta

import httpx
from camunda_client.clients.dto import AuthData
from camunda_client.clients.external_task.client import ExternalTaskClient
from camunda_client.clients.external_task.dto import ExternalTaskConfig
from camunda_client.worker.task_worker import ExternalTaskWorker
from external_task.processor import subscribe


@contextlib.asynccontextmanager
async def suppress_async(*exceptions: type[BaseException]):
    with contextlib.suppress(*exceptions):
        yield


async def main():
    worker_id = "worker-1"
    base_url = "http://localhost:8080/engine-rest"
    username = "demo"
    password = "demo"

    async with httpx.AsyncHTTPTransport() as transport:
        config = ExternalTaskConfig(lock_duration=timedelta(seconds=90))
        client = ExternalTaskClient(
            worker_id=worker_id,
            auth_data=AuthData(username=username, password=password),
            base_url=base_url,
            transport=transport,
            config=config,
        )

        worker = ExternalTaskWorker(
            pull_interval=timedelta(seconds=3),
            client=client,
        )

        async with (
            worker,
            suppress_async(asyncio.CancelledError),
            asyncio.TaskGroup() as tg,
        ):
            tg.create_task(subscribe(task_worker=worker, topic="send-email"))


if __name__ == "__main__":
    asyncio.run(main())
