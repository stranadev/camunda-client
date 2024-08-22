from contextlib import suppress
from datetime import datetime
from typing import Annotated, Any, Generic, Literal, TypeAlias, TypeVar
from uuid import UUID

import orjson
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
)


def _snake_to_camel(name: str) -> str:
    first, *rest = name.split("_")
    return first + "".join(map(str.capitalize, rest))


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=_snake_to_camel,
    )


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


_T = TypeVar("_T", bound=BaseSchema)


def _validate_nullable_list(value: list[_T] | None) -> list[_T]:
    if value is None:
        return []
    return value


MayBeNullableList = Annotated[list[_T], BeforeValidator(_validate_nullable_list)]
OptionalDict: TypeAlias = dict[str, Any] | None
VariableTypes: TypeAlias = Literal[
    "Boolean",
    "Bytes",
    "Short",
    "Integer",
    "Long",
    "Double",
    "Date",
    "String",
    "Null",
    "Object",
    "Json",
]


class VariableValueSchema(BaseSchema):
    value: Any
    type: VariableTypes | None = None
    value_info: OptionalDict = None


TValue = TypeVar("TValue", bound=BaseModel | int | bool | datetime | UUID)


def _process_json_value(value: Any) -> Any:
    with suppress(orjson.JSONDecodeError):
        return orjson.loads(value)

    return value


class TypedVariableValueSchema(BaseSchema, Generic[TValue]):
    value: Annotated[TValue, AfterValidator(_process_json_value)]
    type: VariableTypes | None = None
    value_info: OptionalDict = None


Variables: TypeAlias = dict[str, VariableValueSchema]


TVariables = TypeVar("TVariables", bound=BaseModel)
