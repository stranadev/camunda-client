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
    history_task = "/history/task"
    variable_instances = "/history/variable-instance"

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

    @classmethod
    def submit_task_form(cls, task_id: str) -> str:
        return f"{cls.task}/{task_id}/submit-form"

    @classmethod
    def claim_task(cls, task_id: str) -> str:
        return f"{cls.task}/{task_id}/claim"

    @classmethod
    def unclaim_task(cls, task_id: str) -> str:
        return f"{cls.task}/{task_id}/unclaim"
