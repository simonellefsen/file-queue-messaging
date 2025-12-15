import pytest
from queue_client import QueueConsumer

@pytest.mark.asyncio
async def test_queue_callback(monkeypatch):
    messages = []

    class FakeMessage:
        def __init__(self, body):
            self.body = body.encode()

        def process(self):
            class Ctx:
                async def __aenter__(inner):
                    return inner
                async def __aexit__(inner, exc, val, tb):
                    pass
            return Ctx()

    # Async generator of messages
    async def fake_message_generator():
        yield FakeMessage("hello")

    class FakeQueueIterator:
        async def __aenter__(self):
            # return async iterator
            return fake_message_generator()
        async def __aexit__(self, exc_type, exc, tb):
            pass

    class FakeQueue:
        # iterator() MUST be synchronous and return a context manager
        def iterator(self):
            return FakeQueueIterator()

    class FakeChannel:
        async def declare_queue(self, name, durable=True):
            return FakeQueue()

    class FakeConnection:
        async def channel(self):
            return FakeChannel()

    async def fake_connect(url):
        return FakeConnection()

    monkeypatch.setattr("aio_pika.connect_robust", fake_connect)

    async def callback(data):
        messages.append(data)

    consumer = QueueConsumer("amqp://mock", "test", callback)
    await consumer.start()

    assert messages == ["hello"]

