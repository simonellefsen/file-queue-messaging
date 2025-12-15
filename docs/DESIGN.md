# File Queue Messaging — System Design

## Overview

The project implements a fault-tolerant, asynchronous file replication pipeline:

[input file] → Producer → RabbitMQ Queue → Consumer → [output file]


The system guarantees:

- Every ASCII text line written to the source file eventually appears identically in the output file.
- No duplicates (at-least-once + idempotent file writer).
- Scalable, observable, containerized, and cloud-deployable architecture.

---

## Architecture Components

### 1. Producer Service
- Tails a file using non-blocking asynchronous I/O (`aiofiles`).
- Publishes each new line to RabbitMQ using `aio_pika`.
- Exposes:
  - `/metrics`
  - `/health/live`
  - `/health/ready`

### 2. Consumer Service
- Listens for messages on the same queue.
- Writes lines to output file via async append.
- Exposes the same health and metric endpoints.

### 3. RabbitMQ
- AMQP 0-9-1 durable message broker.
- Provides message persistence and load distribution.
- Supports clustering and monitoring.

---

## Reliability Guarantees

### Message Delivery
RabbitMQ ensures **durable, persistent message storage**:
- Queue is durable.
- Publisher uses persistent AMQP messages.
- Consumer manually acknowledges after writing to disk.

### Handling Failure
- If producer dies → RabbitMQ buffers messages.
- If consumer dies → unacked messages are redelivered.
- If RabbitMQ restarts → messages persist via storage volume.

---

## Scalability

### Horizontal Scaling
- Producer is single-instance (file tailing is not shareable).
- Consumer supports multiple replicas:
  - Messages are load-balanced automatically.

### Queue Backpressure
If the consumer cannot keep up:
- Queue depth increases.
- Autoscaling (HPA) increases number of consumers.

---

## Observability

Metrics include:

| Component | Metric | Description |
|----------|--------|-------------|
| Producer | `producer_lines_read_total` | Total lines read |
| Producer | `producer_queue_publish_latency_seconds` | Publish latency histogram |
| Consumer | `consumer_lines_written_total` | Total lines written |
| Consumer | `consumer_queue_consume_latency_seconds` | Message consumption latency |
| RabbitMQ | Standard queue metrics | Queue depth, consumer count, rate |

Dashboards for Grafana are provided under `/grafana`.

---

## Design Choices & Alternatives

### Why RabbitMQ?
Pros:
- Durable messaging.
- Easy Kubernetes deployment.
- Native AMQP supported by aio-pika.
- Strong monitoring support.

Alternatives:
- **NATS JetStream** — excellent but fewer operational tools.
- **Redis Streams** — fast but persistence guarantees weaker.

RabbitMQ was chosen as the optimal balance.

---

## Technology Choices

| Component | Library | Reason |
|----------|----------|--------|
| Async I/O | `asyncio`, `aiofiles` | Efficient non-blocking file reading/writing |
| Messaging | `aio-pika` | Native async RabbitMQ client |
| Framework | `FastAPI` | Lightweight + metrics/health endpoints |
| Metrics | `prometheus-client` | Standard toolkit |
| Deployment | Docker + K8s + Helm | Cloud-native |

---

## Future Improvements

- Batch writes to output file for even higher throughput.
- Distributed tracing (OpenTelemetry) integration.
- Rate-limiting & circuit-breakers between components.

---


