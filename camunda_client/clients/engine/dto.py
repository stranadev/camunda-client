from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetTaskVariableDTO:
    task_id: UUID
    variable_name: str
    deserialize_value: bool = True
