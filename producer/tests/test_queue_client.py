import pytest
from queue_client import QueuePublisher

@pytest.mark.asyncio
async def test_queue_publish(monkeypatch):
    class MockQueue:
        pass

    class MockChannel:
        def __init__(self):
            self.sent = None

        @property
        def default_exchange(self):
            return self

        async def declare_queue(self, queue_name, durable=True):
            self.queue_name = queue_name
            self.durable = durable
            return MockQueue()

        async def publish(self, msg, routing_key):
            self.sent = msg.body

    class MockConnection:
        def __init__(self):
            self.channel_obj = MockChannel()

        async def channel(self):
            return self.channel_obj

        async def close(self):
            pass

    async def mock_connect(url):
        return MockConnection()

    monkeypatch.setattr("aio_pika.connect_robust", mock_connect)

    publisher = QueuePublisher("amqp://mock", "test")
    await publisher.connect()
    await publisher.publish("hello")

    # Validate publish
    assert publisher.channel.sent == b"hello"
    assert publisher.channel.queue_name == "test"
    assert publisher.channel.durable is True

