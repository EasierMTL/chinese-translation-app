# Chinese-English Translation Web App

Full-stack web application to automatically translate Chinese to English (and vice-versa) with React/Next.js/FastAPI and deep learning models (BERT) and automated cloud API load-testing with AWS EC2, Google Compute Engine, Terraform, and Locust.

Hosted at: https://easiermtl.com/

<video autoPlay={true} loop={true} muted={true} playsInline={true}><source src="./docs/videos/easiermtl_demo.mp4" type="video/mp4" /></video>

## Table of Contents

- [Next.js UI](./ui)
- [Python](./server)
  - [Backend REST API](./server/README.md)
  - [Model Development & Evaluation](https://github.com/EasierMTL/asian_mtl)
  - [Automated Deployments & Load-Testing CLI](./server/loadtest_cli)
- [Terraform Cloud Instances Deployment Configurations and Scripts](./deploy)
  - [AWS Deployment](./deploy/aws)
  - [GCE Deployment](./deploy/gce)
- [Kubernetes + Helm Deployment to Google Kubernetes Engine (GKE)](./deploy/KUBERNETES.md)
  - [Kubernetes Configuration Files](./deploy/k8s)
  - [Guide](./deploy/KUBERNETES.md)
- [Misc. Documentation](./docs)
  - [Research Report](./docs/final_report.md)
  - [Initial Project Proposal](./docs/proposal.md)

## Getting Started

**Make sure you have the following already installed:**

- Frontend
  - `^yarn 1.22.17`
- Backend
  - `^poetry 1.1.11`
- Deployment
  - `docker`
  - `terraform`
  - `aws`
  - `gcloud`
  - `kubectl`

Rest will be installed as long as you follow the documentation.

The full deployment instructions to Google Kubernetes Engine with K8s and Helm are located [here](./deploy/KUBERNETES.md).

If you don't want to use Kubernetes or want to run locally, run the `ui` and `server` separately. See the individual READMEs in [`ui`](./ui) and [`server`](./server) for more information.

## Tech Stack

- Frontend
  - React, Next.js, draft.js
- Backend
  - Python, FastAPI
- Model Development
  - PyTorch, HuggingFace
- Instance Deployment & Load-Testing
  - AWS, GCE, Docker, Terraform
  - Locust
- Actual Deployment
  - Kubernetes + Helm
  - Google Kubernetes Engine (GKE)

## Contributors

- [Joseph Chen (jchen42703)](https://github.com/jchen42703/)
- [Benson Jin (Jinb2)](https://github.com/Jinb2)
