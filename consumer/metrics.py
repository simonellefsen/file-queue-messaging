from prometheus_client import Counter, Histogram, make_asgi_app

LINES_WRITTEN = Counter(
    "consumer_lines_written_total",
    "Total number of lines written to the output file."
)

CONSUME_LATENCY = Histogram(
    "consumer_queue_consume_latency_seconds",
    "Latency for consuming messages from RabbitMQ."
)

metrics_app = make_asgi_app()

