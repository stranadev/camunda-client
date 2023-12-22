import json
from collections.abc import Sequence
from uuid import UUID

import httpx
from pydantic.type_adapter import TypeAdapter

from camunda_client.clients.dto import AuthData
from camunda_client.clients.endpoints import CamundaUrls
from camunda_client.clients.engine.schemas.body import ClaimTaskSchema
from camunda_client.clients.engine.schemas.response import (
    HistoricTaskInstanceSchema,
    TaskSchema,
    VariableInstanceSchema,
)
from camunda_client.clients.schemas import PaginationParams
from camunda_client.types_ import Variables
from camunda_client.utils import raise_for_status

from .schemas import (
    GetHistoryTasksFilterSchema,
    GetTasksFilterSchema,
    ProcessInstanceQuerySchema,
    ProcessInstanceSchema,
    StartProcessInstanceSchema,
)


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
                exclude_none=True,
            ),
        )
        raise_for_status(response)
        adapter = TypeAdapter(list[ProcessInstanceSchema])
        return adapter.validate_python(response.json())

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
        schema: GetTasksFilterSchema,
        pagination: PaginationParams | None = None,
    ) -> Sequence[TaskSchema]:
        """Queries for tasks that fulfill a given filter"""

        pagination_params = (
            pagination.model_dump(mode="json", by_alias=True) if pagination else {}
        )

        response = await self._http_client.post(
            self._urls.task,
            params=pagination_params,
            content=schema.model_dump_json(by_alias=True, exclude_none=True),
        )
        raise_for_status(response)
        adapter = TypeAdapter(list[TaskSchema])
        return adapter.validate_python(response.json())

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
        adapter = TypeAdapter(list[HistoricTaskInstanceSchema])
        return adapter.validate_python(response.json())

    async def get_variable_instances(
        self,
        *,
        process_instance_id: UUID,
        deserialize_values: bool = False,
    ) -> Sequence[VariableInstanceSchema]:
        response = await self._http_client.get(
            self._urls.variable_instances,
            params={
                "process_instance_id": str(process_instance_id),
                "deserializeValues": deserialize_values,
            },
        )
        raise_for_status(response)
        adapter = TypeAdapter(list[VariableInstanceSchema])
        return adapter.validate_python(response.json())

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


# • эндпоинт старта процесса
# • эндпоинт получения списка юзер таск
# эндпоинт получения списка юзер таск через фильтры ?
# • эндпоинт для получения переменных user_task get_variables
# • эндпоинт для завершения task
# • эндпоинт get task history
# • POST /task/{id}/claim
# • POST /task/anId/unclaim


"""


    async def get_user_tasks(self) -> dict[str, Any]:
        raise NotImplementedError

    async def get_variables(self) -> dict[str, Any]:
        raise NotImplementedError

    async def get_process_history(self) -> dict[str, Any]:
        raise NotImplementedError

    async def get_task_count(self, user_id: UUID) -> dict[str, Any]:
        raise NotImplementedError


"""
