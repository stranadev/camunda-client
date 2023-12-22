from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

import httpx

from camunda_client.exceptions import CamundaClientError
from camunda_client.types_ import VariableTypes, VariableValueSchema


def raise_for_status(response: httpx.Response) -> None:
    if response.is_success:
        return

    raise CamundaClientError(
        status_code=response.status_code,
        response_data=response.content,
    )


def camunda_timedelta(delta: timedelta) -> int:
    return int(delta.total_seconds() * 1000)


def deserialize(  # noqa: C901
    value: Any,  # noqa: ANN401
    type_: VariableTypes | None = None,
) -> VariableValueSchema:
    if type_ is not None:
        return VariableValueSchema(value=value, type=type_)

    if isinstance(value, bool):
        type_ = "Boolean"
    elif isinstance(value, datetime):
        type_ = "Date"
        value = to_camunda_datetime(value)
    elif isinstance(value, Decimal | float):
        type_ = "Double"
    elif isinstance(value, int):
        type_ = "Integer"
    elif isinstance(value, dict):
        type_ = "Object"
    elif isinstance(value, str):
        type_ = "String"

    if type_ is None:
        msg = f"Got undefined type: {type(value)}"
        raise ValueError(msg)

    return VariableValueSchema(value=value, type=type_)


def to_camunda_datetime(value: datetime) -> str:
    return value.isoformat(timespec="milliseconds").replace("+00:00", "+0000")
