from typing import Annotated

import aio_pika
import jsons
from fastapi import Depends
from faststream.rabbit import Channel
from faststream.rabbit.fastapi import RabbitRouter
from faststream.rabbit.schemas import RabbitQueue
from rmediator.mediator import Mediator

from ed_optimization.application.features.order.dtos.create_order_dto import \
    CreateOrderDto
from ed_optimization.application.features.order.requests.commands.process_order_command import \
    ProcessOrderCommand
from ed_optimization.common.generic_helpers import get_config
from ed_optimization.common.logging_helpers import get_logger
from ed_optimization.webapi.dependency_setup import mediator

config = get_config()
router = RabbitRouter(config["rabbitmq"]["url"])
create_order_queue = RabbitQueue(
    name=config["rabbitmq"]["queue"], durable=True)

LOG = get_logger()

# Global cache store to persist data across messages
cache_store = {}


@router.subscriber(create_order_queue)
async def create_order(
    model: CreateOrderDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    """
    Subscribes to the create_order_queue and processes incoming order creation requests.
    """
    return await mediator.send(ProcessOrderCommand(model=model))


queue = RabbitQueue(name="cache_queue", durable=True)


@router.subscriber(queue)
async def main(message: aio_pika.IncomingMessage):
    """
    Subscribes to the cache_queue to handle cache 'get' and 'set' operations.
    """
    async with message.process():
        request = jsons.loads(message.body.decode())
        action = request.get("action")
        key = request.get("key")
        response_body = {}

        if action == "get":
            value = cache_store.get(key)
            response_body = {"value": value}
            LOG.info(f"Cache GET: key='{key}', value='{value}'")
        elif action == "set":
            value = request.get("value")
            cache_store[key] = value
            response_body = {"status": "ok"}
            LOG.info(f"Cache SET: key='{key}', value='{value}'")
        else:
            LOG.warning(f"Unknown action received: {action}")
            response_body = {"status": "error", "message": "Unknown action"}

        if message.reply_to:
            # Access the channel from the message's delivery properties
            channel: Channel = message.channel
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=jsons.dumps(response_body).encode(),
                    content_type="application/json",
                    correlation_id=message.correlation_id,
                ),
                routing_key=message.reply_to,
            )
            LOG.info(f"Replied to '{message.reply_to}' with: {response_body}")
