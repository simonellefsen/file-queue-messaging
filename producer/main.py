import asyncio
import os
import aiofiles
from fastapi import FastAPI
import uvicorn
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("producer")

from file_reader import tail_file
from queue_client import QueuePublisher
from metrics import metrics_app, LINES_READ
from health import health_app

INPUT_FILE = "/data/input.txt"
AMQP_URL = "amqp://guest:guest@rabbitmq/"
QUEUE_NAME = "lines"

producer_app = FastAPI()
producer_app.mount("/metrics", metrics_app)
producer_app.mount("/health", health_app)

async def ensure_input_file(path: str):
    """
    Ensures the input file exists so tailing can begin safely.
    """
    if not os.path.exists(path):
        # Create empty file
        logger.warning(f"Input file {path} does not exist. Creating it.")
        async with aiofiles.open(path, "w") as f:
            await f.write("")

async def run_producer():
    logger.info(f"Producer starting. Watching input file: {INPUT_FILE}")
    publisher = QueuePublisher(AMQP_URL, QUEUE_NAME)
    await publisher.connect()
    logger.info(f"Connected to RabbitMQ at {AMQP_URL}, queue '{QUEUE_NAME}'")

    async for line in tail_file(INPUT_FILE):
        logger.info(f"Read line from {INPUT_FILE}: {line!r}")
        LINES_READ.inc()
        await publisher.publish(line)
        logger.info(f"Published line to queue '{QUEUE_NAME}'")

@producer_app.on_event("startup")
async def startup_event():
    await ensure_input_file(INPUT_FILE)
    asyncio.create_task(run_producer())

if __name__ == "__main__":
    uvicorn.run("main:producer_app", host="0.0.0.0", port=8000)

