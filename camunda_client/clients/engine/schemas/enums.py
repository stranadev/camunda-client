from enum import Enum


class ProcessInstanceQuerySortEnum(Enum):
    INSTANCE_ID = "instanceId"
    DEFINITION_ID = "definitionId"
    DEFINITION_KEY = "definitionKey"
    BUSINESS_KEY = "businessKey"
    TENANT_ID = "tenantId"


class State(Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    COMPLETED = "COMPLETED"
    EXTERNALLY_TERMINATED = "EXTERNALLY_TERMINATED"
    INTERNALLY_TERMINATED = "INTERNALLY_TERMINATED"


class TaskQuerySortEnum(Enum):
    TASK_ID = "taskId"
    ACTIVITY_INSTANCE_ID = "activityInstanceId"
    PROCESS_DEFINITION_ID = "processDefinitionId"
    PROCESS_INSTANCE_ID = "processInstanceId"
    EXECUTION_ID = "executionId"
    DURATION = "duration"
    END_TIME = "endTime"
    START_TIME = "startTime"
    TASK_NAME = "taskName"
    TASK_DESCRIPTION = "taskDescription"
    ASSIGNEE = "assignee"
    OWNER = "owner"
    DUE_DATE = "dueDate"
    FOLLOW_UP_DATE = "followUpDate"
    DELETE_REASON = "deleteReason"
    TASK_DEFINITION_KEY = "taskDefinitionKey"
    PRIORITY = "priority"
    CASE_DEFINITION_ID = "caseDefinitionId"
    CASE_INSTANCE_ID = "caseInstanceId"
    CASE_EXECUTION_ID = "caseExecutionId"
    TENANT_ID = "tenantId"


class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"


class Operator(Enum):
    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    GTEQ = "gteq"
    LT = "lt"
    LTEQ = "lteq"
    LIKE = "like"
    NOT_LIKE = "notLike"


class DelegationState(Enum):
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"


class IncidentStatus(Enum):
    OPEN = "open"
    RESOLVED = "resolved"


class SortByHistoricProcessInstance(Enum):
    INSTANCE_ID = "instanceId"
    DEFINITION_ID = "definitionId"
    DEFINITION_KEY = "definitionKey"
    DEFINITION_NAME = "definitionName"
    DEFINITION_VERSION = "definitionVersion"
    BUSINESS_KEY = "businessKey"
    START_TIME = "startTime"
    END_TIME = "endTime"
    DURATION = "duration"
    TENANT_ID = "tenantId"
