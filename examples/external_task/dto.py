from dataclasses import dataclass

from .core_worker import WorkerProtocol


@dataclass(frozen=True, slots=True)
class TopicWorker:
    topic: str
    worker_cls: type[WorkerProtocol]
