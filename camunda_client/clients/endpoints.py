from typing import ClassVar


class ExternalTaskUrls:
    _base_path: ClassVar[str] = "/external-task"

    fetch_and_lock = f"{_base_path}/fetchAndLock"

    @classmethod
    def complete(cls, ident: str) -> str:
        return f"{cls._base_path}/{ident}/complete"

    @classmethod
    def failure(cls, ident: str) -> str:
        return f"{cls._base_path}/{ident}/failure"

    @classmethod
    def extend_lock(cls, ident: str) -> str:
        return f"{cls._base_path}/{ident}/extendLock"

    @classmethod
    def unlock(cls, ident: str) -> str:
        return f"{cls._base_path}/{ident}/unlock"

    @classmethod
    def bpmn_error(cls, ident: str) -> str:
        return f"{cls._base_path}/{ident}/bpmnError"


class CamundaUrls:
    external_task = ExternalTaskUrls()

    deployment_create = "/deployment/create"
    message_send = "/message"
    process_instances = "/process-instance"
    task = "/task"
    tasks_count = f"{task}/count"
    history_task = "/history/task"
    history_process_instance = "/history/process-instance"
    history_variable_instances = "/history/variable-instance"

    @staticmethod
    def get_start_process_instance(
        process_key: str,
        tenant_id: str | None = None,
    ) -> str:
        if tenant_id:
            return f"/process-definition/key/{process_key}/tenant-id/{tenant_id}/start"
        return f"/process-definition/key/{process_key}/start"

    @staticmethod
    def get_process_instance(process_instance_id: str) -> str:
        return f"/process-instance/{process_instance_id}"

    @staticmethod
    def update_process_instance_variables(process_instance_id: str) -> str:
        return f"/process-instance/{process_instance_id}/variables"

    @classmethod
    def get_task_by_id(cls, ident: str) -> str:
        return f"{cls.task}/{ident}"

    @classmethod
    def submit_task_form(cls, task_id: str) -> str:
        return f"{cls.task}/{task_id}/submit-form"

    @classmethod
    def claim_task(cls, task_id: str) -> str:
        return f"{cls.task}/{task_id}/claim"

    @classmethod
    def unclaim_task(cls, task_id: str) -> str:
        return f"{cls.task}/{task_id}/unclaim"

    @classmethod
    def set_assignee_task(cls, task_id: str) -> str:
        return f"{cls.task}/{task_id}/assignee"

    @classmethod
    def task_variable(cls, task_id: str, variable_name: str) -> str:
        return f"{cls.task}/{task_id}/variables/{variable_name}"

    @classmethod
    def local_task_variable(cls, task_id: str, variable_name: str) -> str:
        return f"{cls.task}/{task_id}/localVariables/{variable_name}"

    @classmethod
    def identity_links(cls, task_id: str) -> str:
        return f"{cls.task}/{task_id}/identity-links"
