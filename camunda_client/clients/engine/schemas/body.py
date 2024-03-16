from uuid import UUID

from camunda_client.types_ import BaseSchema, Variables

from .enums import SortOrder, TaskQuerySortEnum


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
    process_instance_business_key: str | None = None
    process_instance_business_key_in: list[str] | None = None
    process_definition_key: str | None = None
    process_definition_key_in: str | None = None


class GetHistoryTasksFilterSchema(BaseSchema):
    process_instance_id: UUID | None = None
    sorting: SortSchema | None = None


class SetAssigneeTaskSchema(BaseSchema):
    user_id: str
