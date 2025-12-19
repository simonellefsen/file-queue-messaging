import aio_pika
import logging
from metrics import PUBLISH_LATENCY

logger = logging.getLogger("producer")

class QueuePublisher:
    def __init__(self, amqp_url: str, queue_name: str):
        self.amqp_url = amqp_url
        self.queue_name = queue_name

    async def connect(self):
        logger.info(f"Connecting to RabbitMQ at {self.amqp_url}")
        self.connection = await aio_pika.connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)

        logger.info(f"Queue declared: {self.queue_name}")

    async def publish(self, text: str):
        message = aio_pika.Message(text.encode())

        logger.info(f"Publishing message: {text!r}")

        with PUBLISH_LATENCY.time():
            await self.channel.default_exchange.publish(
                message, routing_key=self.queue_name
            )

        logger.info(f"Message published to '{self.queue_name}'")

