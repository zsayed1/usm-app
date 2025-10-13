# 🐍 USM App – Python Microservice with GitHub Actions CI/CD and Argo Rollouts

This repository hosts a simple Python microservice built with **Flask**, packaged into a Docker container, and deployed to Kubernetes using **Helm** and **GitOps** principles.  
It demonstrates a complete CI/CD pipeline integrated with **Argo Rollouts** for progressive delivery and **automatic rollback testing**.

---

## 📦 Application Overview

The application exposes a single health endpoint and **intentionally self-terminates after 3 minutes** to simulate a runtime failure — useful for validating rollback behavior.

```python
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def health():
    return "OK", 200

if __name__ == "__main__":
    # Bind host and port from env vars or use defaults
    host = os.getenv("FLASK_BIND_HOST", "0.0.0.0")  # 0.0.0.0 to listen externally
    port = int(os.getenv("FLASK_PORT", 8080))
    # Enable threaded server for better concurrency
    app.run(host=host, port=port, threaded=True)
```

This behavior is used in combination with **Argo Rollouts** to test how the platform reacts to a failed deployment and automatically rolls back to a previous stable version.

---

## ⚙️ Environment Configuration

The `.env` file in the repository contains the application version, which drives the Docker image tag during deployment:

```
APP_VERSION=0.0.1
```

This version is dynamically injected into the CD pipeline to ensure consistent tagging.

---

## 🔁 GitHub Actions Pipelines

The repository includes two GitHub Actions workflows — one for **CI** and one for **CD** — that automate validation, image building, chart packaging, and deployment.

---

### ✅ CI – Validate Python, Docker, and Helm

Location: `.github/workflows/ci.yaml`

Triggered on **every branch push**, this workflow:

- Runs static code analysis with `bandit` and `safety`
- Builds the Docker image to verify it compiles
- Runs `helm lint` to validate Helm chart syntax

This ensures code quality and deployment readiness before merging changes.

---

### 🚀 CD – Build & Push Docker Image and Helm Chart

Location: `.github/workflows/cd.yaml`

Triggered on pushes to `dev`, `master`, or `feature/brokenApp` branches (or via manual dispatch). It:

1. Reads `APP_VERSION` from `.env` and builds a branch-based image tag (e.g., `dev-0.0.1`, `prod-0.0.1`)
2. Authenticates to AWS via **OIDC** (no static credentials)
3. Builds and pushes the Docker image to **Amazon ECR**
4. Packages and pushes the Helm chart to the **ECR OCI Helm registry**

> ⚠️ The **Docker image and Helm chart registry names are hardcoded** here. They are provisioned by the `usm-gitops-infra` repository where ECR resources are created.

---

## 🧪 Simulating Failures with `feature/brokenApp`

A special branch, **`feature/brokenApp`**, exists to deliberately deploy a broken image that crashes after ~3 minutes.  
This is used to **test Argo Rollouts’ automatic rollback capability**.

How to test rollback:

1. Switch to the branch:
   ```bash
   git checkout feature/brokenApp
   ```

2. Make a small commit (e.g., update `README.md`) and push:
   ```bash
   git commit --allow-empty -m "Trigger rollout test"
   git push origin feature/brokenApp
   ```

3. This triggers the **CD pipeline**, which builds and pushes the broken image. This will just push the image, we need to make changes in the https://github.com/zsayed1/usm-gitops-apps to make sure we update the tag.

4. Argo Rollouts attempts the deployment → the pod fails after 3 minutes → rollout **aborts and reverts** to the last healthy ReplicaSet.

This demonstrates how your platform self-heals from bad releases with **zero manual intervention**.

---

## 📦 Build and Run Locally

You can test the service locally before pushing changes:

```bash
docker build -t usm-app .
docker run -p 8080:8080 usm-app
```

Check the health endpoint:

```bash
curl http://localhost:8080/
```

It will return `OK` and then terminate after ~3 minutes.

---

## ⚓ Helm Chart

The Helm chart is in `charts/helm-usm-app` and is packaged and pushed automatically by the CD workflow.  
You can test it locally:

```bash
helm lint charts/helm-usm-app
helm install usm-app charts/helm-usm-app
```

---

## 🔁 End-to-End Flow

1. Developer pushes code → **CI** pipeline runs security scans, Docker build, and Helm lint
2. Merge into `dev`, `master`, or `feature/brokenApp` → **CD** pipeline builds image and chart
3. Docker image and Helm chart pushed to **Amazon ECR**
4. **ArgoCD** syncs the chart into the cluster from https://github.com/zsayed1/usm-gitops-apps. 
5. If the new version fails readiness → rollout aborts and **automatic rollback** happens

---

## 📊 Summary

- ✅ Flask app with simulated failure to test rollout behavior  
- ✅ `.env`-based versioning for Docker image tags  
- ✅ CI workflow ensures Python, Docker, and Helm quality checks  
- ✅ CD workflow automates build and deploy with AWS OIDC authentication  
- ✅ Docker and Helm registries hardcoded from **usm-gitops-infra** provisioning  
- ✅ `feature/brokenApp` branch triggers rollback scenarios without manual changes  

This repository showcases a production-grade CI/CD + GitOps pipeline with built-in rollback safety — ideal for building confidence in your deployment workflows.



