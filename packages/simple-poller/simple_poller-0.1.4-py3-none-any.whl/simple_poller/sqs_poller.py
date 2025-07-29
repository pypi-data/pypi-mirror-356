import gzip
import json
import logging
from asyncio import as_completed
from base64 import b64decode
from collections.abc import Awaitable, Callable
from os import getenv
from typing import Any, Literal, override

import boto3
import simple_zstd as zstd
from box import Box

from .base_poller import BasePoller

STAGE: str = getenv("STAGE", "local")

logger = logging.getLogger(__name__)


class SqsPoller(BasePoller):
    def __init__(
        self,
        queue_url: str,
        handler: Callable[..., Awaitable[None]],
        *,
        client: Any = None,
        raw_message: bool = True,
    ) -> None:
        super().__init__(handler)

        self.__client = client or boto3.client(
            service_name="sqs",
            endpoint_url=(
                "http://localhost:4566" if STAGE == "local"
                else None
            ),
        )

        self.__queue_url: str = (
            queue_url if queue_url.startswith(("https://", "http://"))
            else self.__client.get_queue_url(
                QueueName=queue_url,
            )["QueueUrl"]

        )
        self.__fifo: bool = queue_url.endswith(".fifo")

        self.__raw_message = raw_message

    @staticmethod
    def __decode_body(
        body: str,
        *,
        encoding: Literal["gzip", "zstd"] | None = None,
    ) -> str:
        match encoding:
            case "gzip":
                return gzip.decompress(b64decode(body.encode())).decode()
            case "zstd":
                return zstd.decompress(b64decode(body.encode())).decode()
            case None:
                return body
            case _:
                raise ValueError

    @override
    async def poll(self) -> None:
        messages: list[dict[str, Any]] = self.__client.receive_message(
            MessageAttributeNames=["All"],
            MessageSystemAttributeNames=["All"],
            # Maximum allowed number
            MaxNumberOfMessages=10,
            QueueUrl=self.__queue_url,
            # To enable long polling
            WaitTimeSeconds=1,
        ).get("Messages", [])

        logger.info(f"Received {len(messages)} message")

        to_be_deleted: list[dict[str, str]] = []

        async def process(message: dict[str, Any]) -> None:
            message_id: str = message["MessageId"]
            logger.info(f"Processing message with ID {message_id}")

            try:
                await self.handler(
                    # Use `Box` to provide object-like attribute access (like `message.Body`)
                    # while still being instance of `dict`
                    Box(message)
                    if self.__raw_message
                    else json.loads(self.__decode_body(
                        message["Body"],
                        encoding=(
                            message
                            .get("MessageAttributes", {})
                            .get("ContentEncoding", {})
                            .get("StringValue")
                        ),
                    )),
                )

                to_be_deleted.append({
                    "Id": message_id,
                    "ReceiptHandle": message["ReceiptHandle"],
                })
            except RuntimeError:
                logger.exception(f"Failed to process message with ID {message_id}")

        try:
            if self.__fifo:
                for message in messages:
                    await process(message)
            else:
                # TODO: Use `async for` which is only available in Python 3.13+
                for task in as_completed(process(message) for message in messages):
                    await task
        finally:
            if to_be_deleted:
                self.__client.delete_message_batch(
                    Entries=to_be_deleted,
                    QueueUrl=self.__queue_url,
                )

                logger.info(f"Deleted {len(to_be_deleted)} message")
