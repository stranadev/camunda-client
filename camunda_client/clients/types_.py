from datetime import datetime
from typing import Annotated, TypeVar

from pydantic import PlainSerializer

from camunda_client.utils import to_camunda_datetime

_T = TypeVar("_T")

SerializedDateTime = Annotated[
    datetime,
    PlainSerializer(to_camunda_datetime, return_type="str", when_used="json"),
]

CommaSeparatedStrList = Annotated[
    list[_T], PlainSerializer(lambda v: ",".join(str(i) for i in v))
]
