# Model Jacket

Model Jacket is a lightweight framework that wraps any ML model with a FastAPI server, Docker image, Prometheus metrics, and Kubernetes Helm chart—so you can go from **model file ➜ production endpoint** in minutes.

## Quick Start
```bash
pip install -e .
# Train or load a model and save as TorchScript
python export_model.py  # produces model.pt

jacket build --framework torch --model-path model.pt --tag v1

docker run -p 8000:8000 model-jacket:v1
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"input_data": [[1,2,3]]}'
```

## Features
- 🔌 **Framework‑agnostic** (Torch & ONNX out of the box)
- 🐳 **One‑command containerization** via `jacket build`
- ⚡ **Low‑latency FastAPI** server with async I/O
- 📈 **Built‑in Prometheus metrics** and `/healthz` endpoint
- ☸️ **Production-ready Helm chart** with HPA
- 🛡️ **CI/CD GitHub Action** for automatic build & deploy

---
Feel free to star ⭐, fork 🔱, and contribute! :rocket: