from typing import Annotated, Literal
from uuid import UUID

from pydantic import BeforeValidator


from camunda_client.clients.types_ import SerializedDateTime
from camunda_client.types_ import (
    BaseSchema,
    MayBeNullableList,
    Variables,
    VariableValueSchema,
)
from camunda_client.utils import get_value

from .enums import DelegationState, State


class LinkSchema(BaseSchema):
    rel: str | None = None
    href: str | None = None
    method: str | None = None


class ProcessInstanceSchema(BaseSchema):
    id: UUID
    definition_id: str | None = None
    links: MayBeNullableList[LinkSchema]
    business_key: str | None = None
    case_instance_id: str | None = None
    suspended: bool | None = None
    tenant_id: str | None = None


class HistoricProcessInstanceSchema(BaseSchema):
    id: UUID
    root_process_instance_id: UUID | None = None
    super_process_instance_id: UUID | None = None
    super_case_instance_id: str | None = None
    case_instance_id: str | None = None
    process_definition_name: str | None = None
    process_definition_key: str | None = None
    process_definition_version: int | None = None
    process_definition_id: str | None = None
    business_key: str | None = None
    start_time: SerializedDateTime | None = None
    end_time: SerializedDateTime | None = None
    removal_time: SerializedDateTime | None = None
    duration_in_millis: int | None = None
    start_user_id: str | None = None
    start_activity_id: str | None = None
    delete_reason: str | None = None
    tenant_id: str | None = None
    state: State | None = None


class ProcessDefinitionSchema(BaseSchema):
    id: str
    key: str | None = None
    category: str | None = None
    description: str | None = None
    name: str | None = None
    version: int | None = None
    resource: str | None = None
    deployment_id: str | None = None
    diagram: str | None = None
    suspended: bool | None = None
    tenant_id: str | None = None
    version_tag: str | None = None
    history_time_to_live: str | None = None
    startable_in_task_list: bool | None = None
    variables: Variables


class TaskSchema(BaseSchema):
    id: UUID
    name: str
    assignee: str | None = None
    owner: str | None = None
    created: SerializedDateTime
    due: SerializedDateTime | None = None
    last_updated: SerializedDateTime | None = None
    delegation_state: DelegationState | None = None
    description: str | None = None
    execution_id: UUID
    parent_task_id: str | None = None
    priority: int
    process_definition_id: str
    process_instance_id: UUID
    case_execution_id: str | None = None
    case_definition_id: str | None = None
    case_instance_id: str | None = None
    task_definition_key: str | None = None
    suspended: bool
    tenant_id: str | None

    @property
    def assignee_uuid(self) -> UUID:
        return UUID(get_value(self.assignee))


class HistoricTaskInstanceSchema(BaseSchema):
    id: UUID
    process_definition_key: str
    process_definition_id: str
    process_instance_id: UUID
    execution_id: str
    case_definition_key: str | None = None
    case_definition_id: str | None = None
    case_instance_id: str | None = None
    case_execution_id: str | None = None
    activity_instance_id: str | None = None
    name: str | None = None
    description: str | None = None
    delete_reason: str | None = None
    owner: str | None = None
    assignee: str | None = None
    start_time: SerializedDateTime
    end_time: SerializedDateTime | None = None
    duration: int | None = None
    task_definition_key: str
    priority: int | None = None
    due: SerializedDateTime | None = None
    parent_task_id: str | None = None
    follow_up: SerializedDateTime | None = None
    tenant_id: str | None = None
    removal_time: SerializedDateTime | None = None
    root_process_instance_id: UUID | None = None

    @property
    def assignee_uuid(self) -> UUID:
        return UUID(get_value(self.assignee))


class VariableInstanceSchema(VariableValueSchema):
    id: str
    name: str
    process_definition_id: str
    process_instance_id: UUID
    execution_id: str
    case_instance_id: str | None = None
    case_execution_id: str | None = None
    task_id: str | None = None
    batch_id: str | None = None
    activity_instance_id: str | None = None
    tenant_id: str | None = None
    error_message: str | None = None


class TaskIdentitySchema(BaseSchema):
    user_id: Annotated[UUID | None, BeforeValidator(lambda v: v if v else None)] = None
    group_id: str | None = None
    type: Literal["candidate", "assignee", "owner"]
