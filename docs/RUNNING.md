# Running the File Queue Messaging System

This guide covers:

1. Running locally with Docker Compose
2. Running inside Kubernetes
3. Using the Helm chart

---

## 1. Run Locally (Docker Compose)

### Prerequisites
- Docker
- Docker Compose

### Start the system
```bash
cd docker
docker-compose up --build
```

###nInteract with it

Place a file at:

data/input.txt


Append text:

echo "hello" >> data/input.txt

Check output:

data/output.txt

It will eventually contain:

hello

## 3. Deploy via Helm

### Prerequisites
 - kubectl
 - helm
 - kubernetes cluster (will be using k3d for local development)
 - Prometheus Operator

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
# then install it
helm install monitoring prometheus-community/kube-prometheus-stack
```

### Install chart
```bash
helm install file-queue ./helm
```

### Upgrade chart
```bash
helm upgrade file-queue ./helm
```

### Remove chart
```bash
helm uninstall file-queue
```
