from dataclasses import dataclass

import pytest
from camunda_client.utils import get_value


@dataclass(frozen=True, slots=True)
class Dataclass:
    number: int | None = None


def test_get_value() -> None:
    assert get_value(Dataclass(number=1).number)


def test_get_value_raises() -> None:
    with pytest.raises(ValueError):
        get_value(Dataclass(number=None).number)
