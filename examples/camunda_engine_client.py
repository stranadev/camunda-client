import asyncio
import datetime
import uuid

import httpx

from camunda_client.clients.dto import AuthData
from camunda_client.clients.engine.client import CamundaEngineClient
from camunda_client.utils import deserialize


async def main() -> None:
    base_url = "http://localhost:8080/engine-rest"
    username = "demo"
    password = "demo"

    async with httpx.AsyncHTTPTransport() as transport:
        client = CamundaEngineClient(
            auth_data=AuthData(username=username, password=password),
            base_url=base_url,
            transport=transport,
        )
        result = await client.start_process(
            "NotifyUser",
            variables={
                "email": deserialize("hello-world@gmail.com"),
                "sent_at": deserialize(datetime.datetime.now(tz=datetime.UTC)),
                "event_id": deserialize(str(uuid.uuid4())),
            },
        )
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
