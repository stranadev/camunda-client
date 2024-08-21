import datetime
import random
import uuid
from asyncio import Protocol
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from camunda_client.types_ import Variables
from camunda_client.utils import deserialize
from camunda_client.worker.dto import ExternalTaskDTO


class WorkerProtocol(Protocol):
    async def execute(self, dto: ExternalTaskDTO) -> Any: ...


@dataclass(frozen=True, slots=True)
class ResultDTO:
    is_success: bool
    message: str | None = None
    variables: Variables | None = None


class MessageDTO(BaseModel):
    email: str
    message: str


class EmailService:
    async def send(self, dto: MessageDTO) -> bool:
        print(dto)
        return random.choice([True, False, True, True, True])


class SendEmailWorker:
    def __init__(self) -> None:
        # ↓ Use DI container ↓
        # This initialization is provided as an example
        self._service = EmailService()

    async def execute(self, dto: ExternalTaskDTO) -> ResultDTO:
        message_dto = dto.get_variables(MessageDTO)
        result = await self._service.send(message_dto)
        if result is False:
            return ResultDTO(is_success=result, message="Email wasn't sent")

        return ResultDTO(
            is_success=result,
            variables={
                "sent_at": deserialize(datetime.datetime.now(tz=datetime.UTC)),
                "event_id": deserialize(str(uuid.uuid4())),
            },
        )
