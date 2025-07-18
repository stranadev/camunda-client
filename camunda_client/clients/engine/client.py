import json
from collections.abc import Sequence
from http import HTTPStatus
from typing import Any
from typing_extensions import deprecated
from uuid import UUID

import httpx
from pydantic.type_adapter import TypeAdapter

from camunda_client.clients.dto import AuthData
from camunda_client.clients.endpoints import CamundaUrls
from camunda_client.clients.engine.schemas.body import (
    ClaimTaskSchema,
    HistoricProcessInstanceFilterSchema,
    HistoryVariableInstanceFilterSchema,
    SetAssigneeTaskSchema,
    UpdateProcessVariablesSchema,
)
from camunda_client.clients.engine.schemas.query import (
    HistoryVariableInstanceFilterParamsSchema,
)
from camunda_client.clients.engine.schemas.response import (
    HistoricTaskInstanceSchema,
    TaskIdentitySchema,
    TaskSchema,
    VariableInstanceSchema,
    HistoricProcessInstanceSchema,
)
from camunda_client.clients.schemas import CountSchema, PaginationParams
from camunda_client.types_ import (
    TValue,
    TypedVariableValueSchema,
    VariableValueSchema,
    Variables,
)
from camunda_client.utils import raise_for_status

from .schemas import (
    GetHistoryTasksFilterSchema,
    GetTasksFilterSchema,
    ProcessInstanceQuerySchema,
    ProcessInstanceSchema,
    StartProcessInstanceSchema,
    SendCorrelationMessageSchema,
)
from .dto import GetTaskVariableDTO, UpdateTaskVariableDTO


PROCESS_INSTANCE_ADAPTER = TypeAdapter(list[ProcessInstanceSchema])
TASK_ADAPTER = TypeAdapter(list[TaskSchema])
HISTORIC_TASK_INSTANCE_ADAPTER = TypeAdapter(list[HistoricTaskInstanceSchema])
HISTORIC_PROCESS_INSTANCE_ADAPTER = TypeAdapter(list[HistoricProcessInstanceSchema])
VARIABLE_INSTANCE_ADAPTER = TypeAdapter(list[VariableInstanceSchema])
TASK_IDENTITY_ADAPTER = TypeAdapter(list[TaskIdentitySchema])


class CamundaEngineClient:
    def __init__(
        self,
        base_url: str,
        auth_data: AuthData,
        transport: httpx.AsyncHTTPTransport,
        urls: CamundaUrls | None = None,
    ) -> None:
        self._http_client = httpx.AsyncClient(
            base_url=base_url,
            transport=transport,
            auth=httpx.BasicAuth(
                username=auth_data.username,
                password=auth_data.password,
            ),
            headers={"Content-Type": "application/json"},
        )
        self._urls = urls or CamundaUrls()

    async def start_process(
        self,
        process_key: str,
        business_key: str | None = None,
        variables: Variables | None = None,
        tenant_id: str | None = None,
    ) -> ProcessInstanceSchema:
        """
        Instantiates a given process definition, starts the latest
        version of the process definition which belongs to no tenant.
        Process variables and business key may be supplied in the request body
        """

        url = self._urls.get_start_process_instance(process_key, tenant_id)
        schema = StartProcessInstanceSchema(
            business_key=business_key,
            variables=variables,
        )
        content = schema.model_dump_json(by_alias=True)
        response = await self._http_client.post(url, content=content)
        raise_for_status(response)
        return ProcessInstanceSchema.model_validate(response.json())

    async def get_process_instances(
        self,
        params: ProcessInstanceQuerySchema,
    ) -> Sequence[ProcessInstanceSchema]:
        """
        Queries for process instances that fulfill given parameters.
        Parameters may be static as well as dynamic runtime properties
        of process instances. The size of the result set can be
        retrieved by using the Get Instance Count method
        """

        response = await self._http_client.get(
            self._urls.process_instances,
            params=params.model_dump(
                mode="json",
                by_alias=True,
                exclude_unset=True,
            ),
        )
        raise_for_status(response)
        return PROCESS_INSTANCE_ADAPTER.validate_python(response.json())

    async def delete_process(self, process_instance_id: str) -> None:
        """Deletes a running process instance by id"""

        url = self._urls.get_process_instance(process_instance_id)
        response = await self._http_client.delete(
            url,
            params={"skipCustomListeners": "true", "skipIoMappings": "true"},
        )
        raise_for_status(response)

    async def get_tasks(
        self,
        schema: GetTasksFilterSchema | None = None,
        pagination: PaginationParams | None = None,
    ) -> Sequence[TaskSchema]:
        """Queries for tasks that fulfill a given filter"""
        schema = schema or GetTasksFilterSchema()
        pagination_params = (
            pagination.model_dump(mode="json", by_alias=True) if pagination else {}
        )

        response = await self._http_client.post(
            self._urls.task,
            params=pagination_params,
            content=schema.model_dump_json(by_alias=True, exclude_unset=True),
        )
        raise_for_status(response)
        return TASK_ADAPTER.validate_python(response.json())

    async def update_task(self, task_id: UUID, *, schema: TaskSchema) -> None:
        """Updates a task"""
        response = await self._http_client.put(
            self._urls.task_by_id(task_id),
            content=schema.model_dump_json(by_alias=True),
        )
        raise_for_status(response)

    async def get_tasks_count(
        self,
        schema: GetTasksFilterSchema | None = None,
    ) -> CountSchema:
        """
        Retrieves the number of tasks that fulfill the given filter.
        Corresponds to the size of the result set of the Get Tasks (POST) method and takes the same parameters.
        """
        schema = schema or GetTasksFilterSchema()
        response = await self._http_client.post(
            self._urls.tasks_count,
            content=schema.model_dump_json(by_alias=True, exclude_unset=True),
        )
        raise_for_status(response)
        return CountSchema.model_validate(response.json())

    async def get_task(
        self,
        ident: UUID,
    ) -> TaskSchema | None:
        """Retrieves a task by id"""

        url = self._urls.task_by_id(str(ident))
        response = await self._http_client.get(url)

        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        raise_for_status(response)
        return TaskSchema.model_validate(response.json())

    async def get_history_tasks(
        self,
        schema: GetHistoryTasksFilterSchema,
        pagination: PaginationParams | None = None,
    ) -> Sequence[HistoricTaskInstanceSchema]:
        pagination_params = (
            pagination.model_dump(mode="json", by_alias=True) if pagination else {}
        )

        response = await self._http_client.post(
            self._urls.history_task,
            params=pagination_params,
            content=schema.model_dump_json(by_alias=True),
        )
        raise_for_status(response)
        return HISTORIC_TASK_INSTANCE_ADAPTER.validate_python(response.json())

    async def get_history_process_instances(
        self,
        schema: HistoricProcessInstanceFilterSchema,
        pagination: PaginationParams | None = None,
    ) -> Sequence[HistoricProcessInstanceSchema]:
        pagination_params = (
            pagination.model_dump(mode="json", by_alias=True) if pagination else {}
        )

        response = await self._http_client.post(
            self._urls.history_process_instance,
            params=pagination_params,
            content=schema.model_dump_json(by_alias=True),
        )
        raise_for_status(response)
        return HISTORIC_PROCESS_INSTANCE_ADAPTER.validate_python(response.json())

    @deprecated(
        "Use `get_history_variable_instances` or `get_history_variable_instances_post` instead of this method. Will be removed later.",
    )
    async def get_variable_instances(
        self,
        *,
        process_instance_id: UUID,
        deserialize_values: bool = False,
    ) -> Sequence[VariableInstanceSchema]:
        """Queries for historic variable instances that fulfill the given parameters."""

        response = await self._http_client.get(
            self._urls.history_variable_instances,
            params={
                "processInstanceId": str(process_instance_id),
                "deserializeValues": deserialize_values,
            },
        )
        raise_for_status(response)
        return VARIABLE_INSTANCE_ADAPTER.validate_python(response.json())

    async def get_history_variable_instances(
        self,
        filter_: HistoryVariableInstanceFilterParamsSchema | None = None,
        pagination: PaginationParams | None = None,
    ) -> Sequence[VariableInstanceSchema]:
        """Queries for historic variable instances that fulfill the given parameters."""

        filter_ = filter_ or HistoryVariableInstanceFilterParamsSchema(
            deserialize_values=False
        )
        pagination_params = (
            pagination.model_dump(mode="json", by_alias=True) if pagination else {}
        )
        response = await self._http_client.get(
            self._urls.history_variable_instances,
            params={
                **pagination_params,
                **filter_.model_dump(mode="json", by_alias=True, exclude_unset=True),
            },
        )
        raise_for_status(response)
        return VARIABLE_INSTANCE_ADAPTER.validate_python(response.json())

    async def get_history_variable_instances_post(
        self,
        filter_: HistoryVariableInstanceFilterSchema | None = None,
        pagination: PaginationParams | None = None,
        *,
        deserialize_values: bool = False,
    ) -> Sequence[VariableInstanceSchema]:
        """Queries for historic variable instances that fulfill the given parameters."""

        filter_ = filter_ or HistoryVariableInstanceFilterSchema()
        pagination_params = (
            pagination.model_dump(mode="json", by_alias=True) if pagination else {}
        )
        response = await self._http_client.post(
            self._urls.history_variable_instances,
            params={"deserializeValues": deserialize_values, **pagination_params},
            content=filter_.model_dump_json(by_alias=True, exclude_unset=True),
        )
        raise_for_status(response)
        return VARIABLE_INSTANCE_ADAPTER.validate_python(response.json())

    async def update_variable_instances(
        self,
        *,
        process_instance_id: UUID,
        schema: UpdateProcessVariablesSchema,
    ) -> None:
        """
        Updates or deletes the variables of a process instance by id. Updates precede deletions.
        So, if a variable is updated AND deleted, the deletion overrides the update
        """

        response = await self._http_client.post(
            self._urls.update_process_instance_variables(str(process_instance_id)),
            content=schema.model_dump_json(by_alias=True, exclude_unset=True),
        )
        raise_for_status(response)

    async def submit_task_form(
        self,
        task_id: UUID,
        variables: Variables | None = None,
    ) -> None:
        """
        Completes a task and updates process variables using a form submit.
        """
        variables = variables or {}
        content = json.dumps(
            {
                "variables": {
                    key: value.model_dump(mode="json", by_alias=True)
                    for key, value in variables.items()
                },
            },
        )
        response = await self._http_client.post(
            self._urls.submit_task_form(str(task_id)),
            content=content,
        )
        raise_for_status(response)

    async def claim_task(
        self,
        task_id: UUID,
        user_id: UUID,
    ) -> None:
        """
        Claims a task for a specific user.
        """
        response = await self._http_client.post(
            self._urls.claim_task(str(task_id)),
            content=ClaimTaskSchema(user_id=str(user_id)).model_dump_json(
                by_alias=True,
            ),
        )
        raise_for_status(response)

    async def unclaim_task(
        self,
        task_id: UUID,
    ) -> None:
        """
        Claims a task for a specific user.
        """
        response = await self._http_client.post(self._urls.unclaim_task(str(task_id)))
        raise_for_status(response)

    async def set_assignee_task(
        self,
        task_id: UUID,
        user_id: UUID,
    ) -> None:
        """
        Changes the assignee of a task to a specific user.
        """
        response = await self._http_client.post(
            self._urls.set_assignee_task(str(task_id)),
            content=SetAssigneeTaskSchema(user_id=str(user_id)).model_dump_json(
                by_alias=True,
            ),
        )
        raise_for_status(response)

    async def send_correlation_message(
        self,
        schema: SendCorrelationMessageSchema,
    ) -> dict[str, Any] | None:
        """
        Correlates a message to the process engine to either trigger
        a message start event or an intermediate message catching event.
        """
        response = await self._http_client.post(
            self._urls.message_send,
            content=schema.model_dump_json(by_alias=True, exclude_unset=True),
        )
        raise_for_status(response)

        if response.status_code == HTTPStatus.NO_CONTENT:
            return None

        # if schema.result_enabled is true
        return response.json()

    async def _get_task_variable(
        self,
        dto: GetTaskVariableDTO,
    ) -> httpx.Response:
        url_resolver = self._urls.task_variable
        if dto.is_local_variable:
            url_resolver = self._urls.local_task_variable

        url = url_resolver(task_id=str(dto.task_id), variable_name=dto.variable_name)
        return await self._http_client.get(
            url,
            params={"deserializeValue": dto.deserialize_value},
        )

    async def get_task_variable(
        self,
        dto: GetTaskVariableDTO,
    ) -> VariableValueSchema | None:
        """
        Retrieves a variable from the context of a given task.
        The variable must be visible from the task.
        It is visible from the task if it is a local task
        variable or declared in a parent scope of the task
        """
        response = await self._get_task_variable(dto)
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        raise_for_status(response)
        return VariableValueSchema.model_validate(response.json())

    async def get_typed_task_variable(
        self,
        dto: GetTaskVariableDTO,
        variable_type: type[TValue],
    ) -> TypedVariableValueSchema[TValue] | None:
        """
        Does the same thing as `get_task_variable`,
        except it casts value to the type specified in `variable_type`.
        Note: If you expect to get a pydantic model as the result, set `deserialize_value` to False.
        """
        response = await self._get_task_variable(dto)
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        raise_for_status(response)
        return TypedVariableValueSchema[variable_type].model_validate(response.json())

    async def update_task_variable(
        self,
        dto: UpdateTaskVariableDTO,
    ) -> None:
        """
        Updates a process variable that is visible from the Task scope.
        A variable is visible from the task if it is a local task variable,
        or declared in a parent scope of the task.
        """
        url_resolver = self._urls.task_variable
        if dto.is_local_variable:
            url_resolver = self._urls.local_task_variable

        url = url_resolver(
            task_id=str(dto.task_id),
            variable_name=dto.variable_name,
        )
        content = dto.variable.model_dump_json(by_alias=True)
        response = await self._http_client.put(url, content=content)
        raise_for_status(response)

    async def get_identity_links(
        self,
        task_id: UUID,
    ) -> list[TaskIdentitySchema]:
        url = self._urls.identity_links(str(task_id))
        response = await self._http_client.get(url)
        raise_for_status(response)
        return TASK_IDENTITY_ADAPTER.validate_python(response.json())
