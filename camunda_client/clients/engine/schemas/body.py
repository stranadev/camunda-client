from typing import Annotated
from uuid import UUID

import pydantic

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
    process_definition_key_in: list[str] | None = None
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
    assigned: bool | None = None
    unassigned: bool | None = None
    with_candidate_users: bool | None = None
    without_candidate_users: bool | None = None
    active: bool | None = None


class GetHistoryTasksFilterSchema(BaseSchema):
    task_id: UUID | None = pydantic.Field(None, description="Filter by task id.")
    task_parent_task_id: UUID | None = pydantic.Field(
        None,
        description="Filter by parent task id.",
    )
    process_instance_id: UUID | None = pydantic.Field(
        None,
        description="Filter by process instance id.",
    )
    process_instance_business_key: str | None = pydantic.Field(
        None,
        description="Filter by process instance business key.",
    )
    process_instance_business_key_in: list[str] | None = pydantic.Field(
        None,
        description="Filter by process instances with one of the give business keys.\nThe keys need to be in a comma-separated list.",
    )
    process_instance_business_key_like: str | None = pydantic.Field(
        None,
        description="Filter by  process instance business key that has the parameter value as a substring.",
    )
    execution_id: str | None = pydantic.Field(
        None,
        description="Filter by the id of the execution that executed the task.",
    )
    process_definition_id: str | None = pydantic.Field(
        None,
        description="Filter by process definition id.",
    )
    process_definition_key: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that belong to a process definition with the given key.",
    )
    process_definition_name: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that belong to a process definition with the given name.",
    )
    case_instance_id: str | None = pydantic.Field(
        None,
        description="Filter by case instance id.",
    )
    case_execution_id: str | None = pydantic.Field(
        None,
        description="Filter by the id of the case execution that executed the task.",
    )
    case_definition_id: str | None = pydantic.Field(
        None,
        description="Filter by case definition id.",
    )
    case_definition_key: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that belong to a case definition with the given key.",
    )
    case_definition_name: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that belong to a case definition with the given name.",
    )
    activity_instance_id_in: list[str] | None = pydantic.Field(
        None,
        description="Only include tasks which belong to one of the passed  activity instance ids.",
    )
    task_name: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that have the given name.",
    )
    task_name_like: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that have a name with the given parameter value as substring.",
    )
    task_description: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that have the given description.",
    )
    task_description_like: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that have a description that has the parameter value as a substring.",
    )
    task_definition_key: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that have the given key.",
    )
    task_definition_key_in: list[str] | None = pydantic.Field(
        None,
        description="Restrict to tasks that have one of the passed  task definition keys.",
    )
    task_delete_reason: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that have the given delete reason.",
    )
    task_delete_reason_like: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that have a delete reason that has the parameter value as a substring.",
    )
    task_assignee: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that the given user is assigned to.",
    )
    task_assignee_like: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that are assigned to users with the parameter value as a substring.",
    )
    task_owner: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that the given user owns.",
    )
    task_owner_like: str | None = pydantic.Field(
        None,
        description="Restrict to tasks that are owned by users with the parameter value as a substring.",
    )
    task_priority: int | None = pydantic.Field(
        None,
        description="Restrict to tasks that have the given priority.",
    )
    assigned: bool | None = pydantic.Field(
        None,
        description="If set to `true`, restricts the query to all tasks that are assigned.",
    )
    unassigned: bool | None = pydantic.Field(
        None,
        description="If set to `true`, restricts the query to all tasks that are unassigned.",
    )
    finished: bool | None = pydantic.Field(
        None,
        description="Only include finished tasks. Value may only be `true`, as `false` is the default behavior.",
    )
    unfinished: bool | None = pydantic.Field(
        None,
        description="Only include unfinished tasks. Value may only be `true`, as `false` is the default\nbehavior.",
    )
    process_finished: bool | None = pydantic.Field(
        None,
        description="Only include tasks of finished processes. Value may only be `true`, as `false` is the\ndefault behavior.",
    )
    process_unfinished: bool | None = pydantic.Field(
        None,
        description="Only include tasks of unfinished processes. Value may only be `true`, as `false` is the\ndefault behavior.",
    )
    task_due_date: SerializedDateTime | None = pydantic.Field(
        None,
        description="Restrict to tasks that are due on the given date. By [default](https://docs.camunda.org/manual/7.20/reference/rest/overview/date-format/),\nthe date must have the format `yyyy-MM-dd'T'HH:mm:ss.SSSZ`,\ne.g., `2013-01-23T14:42:45.000+0200`.",
    )
    task_due_date_before: SerializedDateTime | None = pydantic.Field(
        None,
        description="Restrict to tasks that are due before the given date. By [default](https://docs.camunda.org/manual/7.20/reference/rest/overview/date-format/),\nthe date must have the format `yyyy-MM-dd'T'HH:mm:ss.SSSZ`,\ne.g., `2013-01-23T14:42:45.000+0200`.",
    )
    task_due_date_after: SerializedDateTime | None = pydantic.Field(
        None,
        description="Restrict to tasks that are due after the given date. By [default](https://docs.camunda.org/manual/7.20/reference/rest/overview/date-format/),\nthe date must have the format `yyyy-MM-dd'T'HH:mm:ss.SSSZ`,\ne.g., `2013-01-23T14:42:45.000+0200`.",
    )
    without_task_due_date: bool | None = pydantic.Field(
        None,
        description="Only include tasks which have no due date. Value may only be `true`, as `false` is the\ndefault behavior.",
    )
    task_follow_up_date: SerializedDateTime | None = pydantic.Field(
        None,
        description="Restrict to tasks that have a followUp date on the given date. By [default](https://docs.camunda.org/manual/7.20/reference/rest/overview/date-format/),\nthe date must have the format `yyyy-MM-dd'T'HH:mm:ss.SSSZ`,\ne.g., `2013-01-23T14:42:45.000+0200`.",
    )
    task_follow_up_date_before: SerializedDateTime | None = pydantic.Field(
        None,
        description="Restrict to tasks that have a followUp date before the given date. By [default](https://docs.camunda.org/manual/7.20/reference/rest/overview/date-format/),\nthe date must have the format `yyyy-MM-dd'T'HH:mm:ss.SSSZ`,\ne.g., `2013-01-23T14:42:45.000+0200`.",
    )
    task_follow_up_date_after: SerializedDateTime | None = pydantic.Field(
        None,
        description="Restrict to tasks that have a followUp date after the given date. By [default](https://docs.camunda.org/manual/7.20/reference/rest/overview/date-format/),\nthe date must have the format `yyyy-MM-dd'T'HH:mm:ss.SSSZ`,\ne.g., `2013-01-23T14:42:45.000+0200`.",
    )
    started_before: SerializedDateTime | None = pydantic.Field(
        None,
        description="Restrict to tasks that were started before the given date. By [default](https://docs.camunda.org/manual/7.20/reference/rest/overview/date-format/),\nthe date must have the format `yyyy-MM-dd'T'HH:mm:ss.SSSZ`,\ne.g., `2013-01-23T14:42:45.000+0200`.",
    )
    started_after: SerializedDateTime | None = pydantic.Field(
        None,
        description="Restrict to tasks that were started after the given date. By [default](https://docs.camunda.org/manual/7.20/reference/rest/overview/date-format/),\nthe date must have the format `yyyy-MM-dd'T'HH:mm:ss.SSSZ`,\ne.g., `2013-01-23T14:42:45.000+0200`.",
    )
    finished_before: SerializedDateTime | None = pydantic.Field(
        None,
        description="Restrict to tasks that were finished before the given date. By [default](https://docs.camunda.org/manual/7.20/reference/rest/overview/date-format/),\nthe date must have the format `yyyy-MM-dd'T'HH:mm:ss.SSSZ`,\ne.g., `2013-01-23T14:42:45.000+0200`.",
    )
    finished_after: SerializedDateTime | None = pydantic.Field(
        None,
        description="Restrict to tasks that were finished after the given date. By [default](https://docs.camunda.org/manual/7.20/reference/rest/overview/date-format/),\nthe date must have the format `yyyy-MM-dd'T'HH:mm:ss.SSSZ`,\ne.g., `2013-01-23T14:42:45.000+0200`.",
    )
    tenant_id_in: list[str] | None = pydantic.Field(
        None,
        description="Filter by a  list of tenant ids. A task instance must have one of the given\ntenant ids.",
    )
    without_tenant_id: bool | None = pydantic.Field(
        None,
        description="Only include historic task instances that belong to no tenant. Value may only be\n`true`, as `false` is the default behavior.",
    )
    task_variables: list[VariableParameterSchema] | None = pydantic.Field(
        None,
        description="Only include tasks that have variables with certain values. Variable filtering expressions are\ncomma-separated and are structured as follows:\n\nA valid parameter value has the form `key_operator_value`.\n`key` is the variable name, `operator` is the comparison operator to be used\nand `value` the variable value.\n**Note:** Values are always treated as `String` objects on server side.\n\n\nValid operator values are:\n* `eq` - equal to;\n* `neq` - not equal to;\n* `gt` - greater than;\n* `gteq` - greater than or equal to;\n* `lt` - lower than;\n* `lteq` - lower than or equal to;\n* `like`.\n\n`key` and `value` may not contain underscore or comma characters.",
    )
    process_variables: list[VariableParameterSchema] | None = pydantic.Field(
        None,
        description="Only include tasks that belong to process instances that have variables with certain\nvalues. Variable filtering expressions are comma-separated and are structured as\nfollows:\n\nA valid parameter value has the form `key_operator_value`.\n`key` is the variable name, `operator` is the comparison operator to be used\nand `value` the variable value.\n**Note:** Values are always treated as `String` objects on server side.\n\n\nValid operator values are:\n* `eq` - equal to;\n* `neq` - not equal to;\n* `gt` - greater than;\n* `gteq` - greater than or equal to;\n* `lt` - lower than;\n* `lteq` - lower than or equal to;\n* `like`;\n* `notLike`.\n\n`key` and `value` may not contain underscore or comma characters.",
    )
    variable_names_ignore_case: bool | None = pydantic.Field(
        None,
        description="Match the variable name provided in `taskVariables` and `processVariables` case-\ninsensitively. If set to `true` **variableName** and **variablename** are\ntreated as equal.",
    )
    variable_values_ignore_case: bool | None = pydantic.Field(
        None,
        description="Match the variable value provided in `taskVariables` and `processVariables` case-\ninsensitively. If set to `true` **variableValue** and **variablevalue** are\ntreated as equal.",
    )
    task_involved_user: str | None = pydantic.Field(
        None,
        description="Restrict to tasks with a historic identity link to the given user.",
    )
    task_involved_group: str | None = pydantic.Field(
        None,
        description="Restrict to tasks with a historic identity link to the given group.",
    )
    task_had_candidate_user: str | None = pydantic.Field(
        None,
        description="Restrict to tasks with a historic identity link to the given candidate user.",
    )
    task_had_candidate_group: str | None = pydantic.Field(
        None,
        description="Restrict to tasks with a historic identity link to the given candidate group.",
    )
    with_candidate_groups: bool | None = pydantic.Field(
        None,
        description="Only include tasks which have a candidate group. Value may only be `true`,\nas `false` is the default behavior.",
    )
    without_candidate_groups: bool | None = pydantic.Field(
        None,
        description="Only include tasks which have no candidate group. Value may only be `true`,\nas `false` is the default behavior.",
    )
    or_queries: list["GetHistoryTasksFilterSchema"] | None = pydantic.Field(
        None,
        description="A JSON array of nested historic task instance queries with OR semantics.\n\nA task instance matches a nested query if it fulfills at least one of the query's predicates.\n\nWith multiple nested queries, a task instance must fulfill at least one predicate of each query\n([Conjunctive Normal Form](https://en.wikipedia.org/wiki/Conjunctive_normal_form)).\n\nAll task instance query properties can be used except for: `sorting`, `withCandidateGroups`, ` withoutCandidateGroups`.\n\nSee the [User Guide](https://docs.camunda.org/manual/7.20/user-guide/process-engine/process-engine-api/#or-queries) for more information about OR queries.",
    )
    sorting: list[SortSchema] | None = pydantic.Field(
        None,
        description="An array of criteria to sort the result by. Each element of the array is\n                    an object that specifies one ordering. The position in the array\n                    identifies the rank of an ordering, i.e., whether it is primary, secondary,\n                    etc. Sorting has no effect for `count` endpoints",
    )


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
    started_before: SerializedDateTime | None = None
    started_after: SerializedDateTime | None = None
    finished_before: SerializedDateTime | None = None
    finished_after: SerializedDateTime | None = None
    executed_activity_after: SerializedDateTime | None = None
    executed_activity_before: SerializedDateTime | None = None
    executed_job_after: SerializedDateTime | None = None
    executed_job_before: SerializedDateTime | None = None
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


class HistoryVariableInstanceFilterSchema(BaseSchema):
    variable_name: str | None = None
    variable_name_like: str | None = None
    variable_name_in: list[str] | None = None
    variable_value: str | None = None
    process_instance_id: UUID | None = None
    process_instance_id_in: list[UUID] | None = None
    task_id_in: list[UUID] | None = None

    # ↓ useless field ↓
    deserialize_values: Annotated[bool | None, pydantic.Field(deprecated=True)] = None
    # ↑ useless field ↑

    include_deleted: bool | None = None
    tenant_id_in: list[str] | None = None
