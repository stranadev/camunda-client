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
    ASSIGNEE = "assignee"
    CASE_EXECUTION_ID = "caseExecutionId"
    CASE_EXECUTION_VARIABLE = "caseExecutionVariable"
    CASE_INSTANCE_ID = "caseInstanceId"
    CASE_INSTANCE_VARIABLE = "caseInstanceVariable"
    CREATED = "created"
    DESCRIPTION = "description"
    DUE_DATE = "dueDate"
    EXECUTION_ID = "executionId"
    EXECUTION_VARIABLE = "executionVariable"
    FOLLOW_UP_DATE = "followUpDate"
    ID = "id"
    INSTANCE_ID = "instanceId"
    LAST_UPDATED = "lastUpdated"
    NAME = "name"
    NAME_CASE_INSENSITIVE = "nameCaseInsensitive"
    PRIORITY = "priority"
    PROCESS_VARIABLE = "processVariable"
    TASK_VARIABLE = "taskVariable"


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
