from camunda_client.worker import ExternalTaskWorker

from .enums import WorkerEnum


async def subscribe(
    topic: str,
    task_worker: ExternalTaskWorker,
) -> None:
    mapping = WorkerEnum.workers()
    async with task_worker.subscribe(topic) as task_contexts:
        async for task_context in task_contexts:
            async with task_context as task_dto:
                worker_cls = mapping[task_dto.topic_name]

                # Resolve the dependency on the DI container.
                # This initialization is provided as an example.
                worker = worker_cls()
                result = await worker.execute(task_dto)

                if result.is_success is False:
                    print(f"Task with id {task_dto.id} was failed")
                    await task_context.fail(error_message=result.message)
                else:
                    print(f"Task with id {task_dto.id} was completed")
                    await task_context.complete(global_variables=result.variables)
