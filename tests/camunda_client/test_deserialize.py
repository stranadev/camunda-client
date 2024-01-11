from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import pytest

from camunda_client.types_ import VariableTypes, VariableValueSchema
from camunda_client.utils import deserialize, to_camunda_datetime

VARIABLE_TYPES = [
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


@pytest.mark.parametrize(
    ["variable_type", "value", "expected"],
    [
        ("Boolean", True, VariableValueSchema(value=True, type="Boolean")),
        ("Bytes", b"1", VariableValueSchema(value=b"1", type="Bytes")),
        ("Short", 1, VariableValueSchema(value=1, type="Short")),
        ("Integer", 1, VariableValueSchema(value=1, type="Integer")),
        ("Long", 1, VariableValueSchema(value=1, type="Long")),
        ("Double", 7.8, VariableValueSchema(value=7.8, type="Double")),
        (
            "Date",
            datetime(2000, 1, 1, tzinfo=UTC),
            VariableValueSchema(value=datetime(2000, 1, 1, tzinfo=UTC), type="Date"),
        ),
        ("String", "Foo", VariableValueSchema(value="Foo", type="String")),
        ("Null", None, VariableValueSchema(value=None, type="Null")),
        (
            "Object",
            {"foo": "bar"},
            VariableValueSchema(value={"foo": "bar"}, type="Object"),
        ),
        (
            "Json",
            '{"foo": "bar"}',
            VariableValueSchema(value='{"foo": "bar"}', type="Json"),
        ),
    ],
)
def test_deserialize_with_type(
    variable_type: VariableTypes,
    value: Any,  # noqa: ANN401
    expected: VariableValueSchema,
) -> None:
    assert deserialize(value=value, type_=variable_type) == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        (True, VariableValueSchema(value=True, type="Boolean")),
        (b"1", VariableValueSchema(value=b"1", type="Bytes")),
        (1, VariableValueSchema(value=1, type="Integer")),
        (7.8, VariableValueSchema(value=7.8, type="Double")),
        (Decimal("7.8"), VariableValueSchema(value=Decimal("7.8"), type="Double")),
        (
            datetime(2000, 1, 1, tzinfo=UTC),
            VariableValueSchema(
                value=to_camunda_datetime(datetime(2000, 1, 1, tzinfo=UTC)),
                type="Date",
            ),
        ),
        ("Foo", VariableValueSchema(value="Foo", type="String")),
        (None, VariableValueSchema(value=None, type="Null")),
        ({"foo": "bar"}, VariableValueSchema(value=b'{"foo":"bar"}', type="Json")),
    ],
)
def test_deserialize(
    value: Any,  # noqa: ANN401
    expected: VariableValueSchema,
) -> None:
    assert deserialize(value=value) == expected
