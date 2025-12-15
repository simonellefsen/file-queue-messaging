import aio_pika

class QueueConsumer:
    def __init__(self, amqp_url: str, queue_name: str, callback):
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        self.callback = callback

    async def start(self):
        connection = await aio_pika.connect_robust(self.amqp_url)
        channel = await connection.channel()
        queue = await channel.declare_queue(self.queue_name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await self.callback(message.body.decode())

