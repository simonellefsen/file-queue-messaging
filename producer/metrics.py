from prometheus_client import Counter, Histogram, make_asgi_app

LINES_READ = Counter(
    "producer_lines_read_total",
    "Total number of lines read from the input file."
)

PUBLISH_LATENCY = Histogram(
    "producer_queue_publish_latency_seconds",
    "Latency of publishing messages to RabbitMQ."
)

metrics_app = make_asgi_app()

