from datetime import datetime
from uuid import UUID

from camunda_client.clients.engine.schemas.query import (
    SortingHistoricProcessInstanceSchema,
    VariableParameterSchema,
)
from camunda_client.clients.types_ import SerializedDateTime
from camunda_client.types_ import BaseSchema, Variables

from .enums import IncidentStatus, SortOrder, TaskQuerySortEnum


class StartProcessInstanceSchema(BaseSchema):
    business_key: str | None = None
    variables: Variables | None = None


class ClaimTaskSchema(BaseSchema):
    user_id: str


class SortSchema(BaseSchema):
    sort_by: TaskQuerySortEnum | None = None
    sort_order: SortOrder | None = None


class GetTasksFilterSchema(BaseSchema):
    assignee: str | None = None
    candidate_group: str | None = None
    candidate_user: str | None = None
    sorting: SortSchema | None = None
    process_instance_id: UUID | None = None
    process_instance_id_in: list[UUID] | None = None
    process_instance_business_key: str | None = None
    process_instance_business_key_in: list[str] | None = None
    process_definition_key: str | None = None
    process_definition_key_in: str | None = None
    task_variables: list[VariableParameterSchema] | None = None
    process_variables: list[VariableParameterSchema] | None = None

    due_date: SerializedDateTime | None = None
    due_date_expression: str | None = None

    due_after: SerializedDateTime | None = None
    due_after_expression: str | None = None

    due_before: SerializedDateTime | None = None
    due_before_expression: str | None = None
    without_due_date: bool | None = None

    created_on: SerializedDateTime | None = None
    created_after: SerializedDateTime | None = None
    created_before: SerializedDateTime | None = None

    task_definition_key: str | None = None
    task_definition_key_like: str | None = None
    task_definition_key_in: list[str] | None = None
    or_queries: list["GetTasksFilterSchema"] | None = None


class GetHistoryTasksFilterSchema(BaseSchema):
    process_instance_id: UUID | None = None
    sorting: SortSchema | None = None


class SetAssigneeTaskSchema(BaseSchema):
    user_id: str


class SendCorrelationMessageSchema(BaseSchema):
    message_name: str
    business_key: str | None = None
    process_instance_id: UUID | None = None

    tenant_id: str | None = None
    without_tenant_id: bool = False

    correlation_keys: Variables | None = None
    local_correlation_keys: Variables | None = None
    process_variables: Variables | None = None
    process_variables_local: Variables | None = None

    all: bool = False
    result_enabled: bool = False
    variables_in_result_enabled: bool = False


class HistoricProcessInstanceFilterSchema(BaseSchema):
    process_instance_id: str | None = None
    process_instance_ids: list[str] | None = None
    process_definition_id: str | None = None
    process_definition_key: str | None = None
    process_definition_key_in: list[str] | None = None
    process_definition_name: str | None = None
    process_definition_name_like: str | None = None
    process_definition_key_not_in: list[str] | None = None
    process_instance_business_key: str | None = None
    process_instance_business_key_in: list[str] | None = None
    process_instance_business_key_like: str | None = None
    root_process_instances: bool | None = None
    finished: bool | None = None
    unfinished: bool | None = None
    with_incidents: bool | None = None
    with_root_incidents: bool | None = None
    incident_type: str | None = None
    incident_status: IncidentStatus | None = None
    incident_message: str | None = None
    incident_message_like: str | None = None
    started_before: datetime | None = None
    started_after: datetime | None = None
    finished_before: datetime | None = None
    finished_after: datetime | None = None
    executed_activity_after: datetime | None = None
    executed_activity_before: datetime | None = None
    executed_job_after: datetime | None = None
    executed_job_before: datetime | None = None
    started_by: str | None = None
    super_process_instance_id: str | None = None
    sub_process_instance_id: str | None = None
    super_case_instance_id: str | None = None
    sub_case_instance_id: str | None = None
    case_instance_id: str | None = None
    tenant_id_in: list[str] | None = None
    without_tenant_id: bool | None = None
    executed_activity_id_in: list[str] | None = None
    active_activity_id_in: list[str] | None = None
    active: bool | None = None
    suspended: bool | None = None
    completed: bool | None = None
    externally_terminated: bool | None = None
    internally_terminated: bool | None = None
    variables: list[VariableParameterSchema] | None = None
    variable_names_ignore_case: bool | None = None
    variable_values_ignore_case: bool | None = None
    sorting: list[SortingHistoricProcessInstanceSchema] | None = None


class UpdateProcessVariablesSchema(BaseSchema):
    modifications: Variables | None = None
    deletions: list[str] | None = None
