from dataclasses import dataclass
from uuid import UUID

from camunda_client.types_ import VariableValueSchema


@dataclass(frozen=True, slots=True)
class GetTaskVariableDTO:
    task_id: UUID
    variable_name: str
    deserialize_value: bool = True
    is_local_variable: bool = False


@dataclass(frozen=True, slots=True)
class UpdateTaskVariableDTO:
    task_id: UUID
    variable_name: str
    variable: VariableValueSchema
    is_local_variable: bool = False
