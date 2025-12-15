import aio_pika
from aio_pika import Message
import asyncio

class QueuePublisher:
    def __init__(self, amqp_url: str, queue_name: str):
        self.amqp_url = amqp_url
        self.queue_name = queue_name

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)

    async def publish(self, text: str):
        msg = Message(text.encode())
        await self.channel.default_exchange.publish(msg, routing_key=self.queue_name)

    async def close(self):
        await self.connection.close()

