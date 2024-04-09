from typing import Any

from pydantic import ConfigDict

from camunda_client.types_ import BaseSchema

from .enums import (
    Operator,
    ProcessInstanceQuerySortEnum,
    SortByHistoricProcessInstance,
    SortOrder,
)


class ConditionQueryParameterSchema(BaseSchema):
    model_config = ConfigDict(use_enum_values=True)

    operator: Operator
    value: Any


class VariableParameterSchema(ConditionQueryParameterSchema):
    name: str | None = None


class ProcessInstanceQuerySortItemSchema(BaseSchema):
    model_config = ConfigDict(use_enum_values=True)

    sort_by: ProcessInstanceQuerySortEnum | None = None
    sort_order: SortOrder | None = None


class ProcessInstanceQuerySchema(BaseSchema):
    deployment_id: str | None = None
    process_definition_id: str | None = None
    process_definition_key: str | None = None
    process_definition_key_in: list[str] | None = None
    process_definition_key_not_in: list[str] | None = None
    business_key: str | None = None
    business_key_like: str | None = None
    case_instance_id: str | None = None
    super_process_instance: str | None = None
    sub_process_instance: str | None = None
    super_case_instance: str | None = None
    sub_case_instance: str | None = None
    active: bool | None = None
    suspended: bool | None = None
    process_instance_ids: list[str] | None = None
    with_incident: bool | None = None
    incident_id: str | None = None
    incident_type: str | None = None
    incident_message: str | None = None
    incident_message_like: str | None = None
    tenant_id_in: list[str] | None = None
    without_tenant_id: bool | None = None
    process_definition_without_tenant_id: bool | None = None
    activity_id_in: list[str] | None = None
    root_process_instances: bool | None = None
    leaf_process_instances: bool | None = None
    variables: list[VariableParameterSchema] | None = None
    variable_names_ignore_case: bool | None = None
    variable_values_ignore_case: bool | None = None
    or_queries: list["ProcessInstanceQuerySchema"] | None = None
    sorting: list[ProcessInstanceQuerySortItemSchema] | None = None


class SortingHistoricProcessInstanceSchema(BaseSchema):
    sortBy: SortByHistoricProcessInstance | None = None
    sortOrder: SortOrder | None = None
