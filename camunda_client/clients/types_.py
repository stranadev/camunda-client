from datetime import datetime
from typing import Annotated

from pydantic import PlainSerializer

from camunda_client.utils import to_camunda_datetime


SerializedDateTime = Annotated[
    datetime,
    PlainSerializer(to_camunda_datetime, return_type="str", when_used="json"),
]
