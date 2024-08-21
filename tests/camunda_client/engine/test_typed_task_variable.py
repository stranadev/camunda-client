from datetime import datetime
from typing import Any
from uuid import UUID

import pytest

from camunda_client.types_ import TypedVariableValueSchema


@pytest.mark.parametrize(
    ("variable_type", "value", "expected"),
    [
        (int, "888", 888),
        (int | None, "888", 888),
        (int | None, None, None),
        (
            UUID,
            "29b34aa1-0eae-42d9-9e97-8b6c028e4841",
            UUID("29b34aa1-0eae-42d9-9e97-8b6c028e4841"),
        ),
        (str, "888", "888"),
        (datetime, datetime.min.isoformat(), datetime.min),
    ],
)
def test_typed(
    variable_type: type[Any],
    value: Any,
    expected: Any,
) -> None:
    response = {"type": "String", "value": value, "valueInfo": {}}
    schema = TypedVariableValueSchema[variable_type].model_validate(response)
    assert isinstance(schema.value, variable_type)
    assert schema.value == expected
