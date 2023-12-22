from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CamundaClientError(Exception):
    status_code: int
    response_data: Any = None

    def __str__(self) -> str:
        return f"HTTP CODE: {self.status_code}, RESPONSE DATA: {self.response_data}"


class InvalidStateError(Exception):
    pass
