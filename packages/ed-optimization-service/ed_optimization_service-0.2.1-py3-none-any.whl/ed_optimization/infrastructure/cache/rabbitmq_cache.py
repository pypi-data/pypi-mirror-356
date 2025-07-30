import asyncio
import uuid
from typing import Generic, TypeVar

import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from ed_infrastructure.documentation.api.endpoint_client import jsons

from ed_optimization.application.contracts.infrastructure.cache.abc_cache import \
    ABCCache

T = TypeVar("T")


class RabbitMQCache(Generic[T], ABCCache[T]):
    def __init__(self, rabbitmq_url: str = "amqp://guest:guest@localhost/"):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None
        self.queue = None
        self.callback_queue = None
        self.futures = {}

    async def _connect(self):
        if self.connection and not self.connection.is_closed:
            return
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue("cache_requests", durable=True)
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.consume(self._on_response)

    async def _on_response(self, message: AbstractIncomingMessage):
        async with message.process():
            correlation_id = message.correlation_id
            if correlation_id in self.futures:
                future = self.futures.pop(correlation_id)
                future.set_result(jsons.loads(message.body.decode()))

    async def get(self, key: str) -> T | None:
        assert self.channel is not None, "RabbitMQ Channel is None"
        assert self.callback_queue is not None, "RabbitMQ callback_queue is None"
        assert self.queue is not None, "RabbitMQ queue is None"

        await self._connect()
        correlation_id = str(uuid.uuid4())
        future = asyncio.Future()
        self.futures[correlation_id] = future

        message_body = {"action": "get", "key": key}

        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=jsons.dumps(message_body).encode(),
                content_type="application/json",
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
            ),
            routing_key=self.queue.name,
        )
        result = await future
        return result.get("value")

    async def set(self, key: str, value: T) -> None:
        assert self.channel is not None, "RabbitMQ Channel is None"
        assert self.queue is not None, "RabbitMQ queue is None"

        await self._connect()
        message_body = {"action": "set", "key": key, "value": value}
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=jsons.dumps(message_body).encode(),
                content_type="application/json",
            ),
            routing_key=self.queue.name,
        )

    async def close(self):
        if self.connection:
            await self.connection.close()
