import aio_pika
import asyncio
import logging
import random
from metrics import CONSUME_LATENCY

logger = logging.getLogger("consumer")


class QueueConsumer:
    def __init__(self, amqp_url: str, queue_name: str, callback):
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        self.callback = callback

    async def start(self):
        logger.info(f"Connecting to RabbitMQ at {self.amqp_url}")
        connection = await aio_pika.connect_robust(self.amqp_url)
        channel = await connection.channel()
        queue = await channel.declare_queue(self.queue_name, durable=True)

        logger.info(f"Consuming queue '{self.queue_name}'")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    with CONSUME_LATENCY.time():
                        body = message.body.decode()
                        logger.info(f"Consuming message: {body!r}")

                        # Introduce artificial random latency (0.1–1.0 seconds)
                        delay = random.uniform(0.1, 1.0)
                        logger.info(f"Simulating processing delay: {delay:.3f}s")
                        await asyncio.sleep(delay)

                        await self.callback(body)
