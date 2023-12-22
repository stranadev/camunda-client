import enum

from .core_worker import SendEmailWorker, WorkerProtocol
from .dto import TopicWorker


class WorkerEnum(enum.Enum):
    send_email = TopicWorker(
        topic="send-email",
        worker_cls=SendEmailWorker,
    )

    @classmethod
    def workers(
        cls,
    ) -> dict[str, type[WorkerProtocol]]:
        return {item.value.topic: item.value.worker_cls for item in cls}
