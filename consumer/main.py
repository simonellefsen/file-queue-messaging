import asyncio
from fastapi import FastAPI
import uvicorn

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("consumer")

from file_writer import append_line
from queue_client import QueueConsumer
from metrics import metrics_app, LINES_WRITTEN
from health import health_app

OUTPUT_FILE = "/data/output.txt"
AMQP_URL = "amqp://guest:guest@rabbitmq/"
QUEUE_NAME = "lines"

consumer_app = FastAPI()
consumer_app.mount("/metrics", metrics_app)
consumer_app.mount("/health", health_app)

async def on_message(line: str):
    logger.info(f"Received message from queue: {line!r}")
    LINES_WRITTEN.inc()
    await append_line(OUTPUT_FILE, line)
    logger.info(f"Wrote line to output file {OUTPUT_FILE}")

async def start_consumer():
    consumer = QueueConsumer(AMQP_URL, QUEUE_NAME, on_message)
    await consumer.start()

@consumer_app.on_event("startup")
async def startup():
    logger.info(f"Consumer starting. Output file is: {OUTPUT_FILE}")
    asyncio.create_task(start_consumer())

if __name__ == "__main__":
    uvicorn.run("main:consumer_app", host="0.0.0.0", port=8001)

