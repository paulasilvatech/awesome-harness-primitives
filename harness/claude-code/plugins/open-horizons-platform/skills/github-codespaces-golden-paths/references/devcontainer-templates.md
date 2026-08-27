# Codespaces Devcontainer Templates

Moved from `codespaces-golden-paths/SKILL.md` to keep the skill body lean for progressive disclosure.

## 2. devcontainer.json Templates by Type

### Python / FastAPI Microservice
```json
{
  "name": "Python Microservice",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "features": {
    "ghcr.io/devcontainers/features/azure-cli:1": {},
    "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.pylint",
        "charliermarsh.ruff",
        "redhat.vscode-yaml",
        "ms-azuretools.vscode-docker",
        "github.copilot"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.testing.pytestEnabled": true
      }
    }
  },
  "postCreateCommand": "pip install -r requirements.txt && pip install -e '.[dev]'",
  "forwardPorts": [8000, 5432],
  "portsAttributes": {
    "8000": { "label": "API Server", "onAutoForward": "notify" }
  }
}
```

### Node.js / Web Application
```json
{
  "name": "Node.js Web App",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
  "features": {
    "ghcr.io/devcontainers/features/azure-cli:1": {},
    "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "bradlc.vscode-tailwindcss",
        "ms-azuretools.vscode-docker",
        "github.copilot"
      ]
    }
  },
  "postCreateCommand": "npm ci",
  "forwardPorts": [3000],
  "portsAttributes": {
    "3000": { "label": "Dev Server", "onAutoForward": "openBrowser" }
  }
}
```

### Terraform / Infrastructure
```json
{
  "name": "Terraform Infrastructure",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/azure-cli:1": {},
    "ghcr.io/devcontainers/features/terraform:1": { "version": "1.7" },
    "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "hashicorp.terraform",
        "redhat.vscode-yaml",
        "github.copilot",
        "ms-azuretools.vscode-azureterraform"
      ]
    }
  },
  "postCreateCommand": "terraform init"
}
```

### Java / Spring Boot Microservice
```json
{
  "name": "Java Microservice",
  "image": "mcr.microsoft.com/devcontainers/java:21",
  "features": {
    "ghcr.io/devcontainers/features/azure-cli:1": {},
    "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/maven:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "vscjava.vscode-java-pack",
        "vmware.vscode-spring-boot",
        "redhat.vscode-yaml",
        "ms-azuretools.vscode-docker",
        "github.copilot"
      ]
    }
  },
  "postCreateCommand": "mvn dependency:resolve",
  "forwardPorts": [8080],
  "portsAttributes": {
    "8080": { "label": "Spring Boot", "onAutoForward": "notify" }
  }
}
```

### AI / ML Pipeline
```json
{
  "name": "AI ML Pipeline",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "features": {
    "ghcr.io/devcontainers/features/azure-cli:1": {},
    "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-toolsai.jupyter",
        "ms-toolsai.vscode-ai",
        "charliermarsh.ruff",
        "github.copilot"
      ],
      "settings": {
        "python.testing.pytestEnabled": true,
        "jupyter.askForKernelRestart": false
      }
    }
  },
  "postCreateCommand": "pip install -r requirements.txt && pip install azure-ai-ml azure-identity mlflow",
  "forwardPorts": [8888, 5000],
  "portsAttributes": {
    "8888": { "label": "Jupyter", "onAutoForward": "notify" },
    "5000": { "label": "MLflow", "onAutoForward": "notify" }
  }
}
```

### Data Pipeline
```json
{
  "name": "Data Pipeline",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "features": {
    "ghcr.io/devcontainers/features/azure-cli:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-toolsai.jupyter",
        "charliermarsh.ruff",
        "redhat.vscode-yaml",
        "github.copilot"
      ]
    }
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "forwardPorts": [8080, 4040],
  "portsAttributes": {
    "4040": { "label": "Spark UI", "onAutoForward": "notify" }
  }
}
```

---

## 3. Skeleton Integration

Each Golden Path template skeleton should include:

```
skeleton/
├── .devcontainer/
│   └── devcontainer.json    # Type-specific config
├── .github/
│   └── workflows/
│       └── ci.yaml          # CI pipeline
├── catalog-info.yaml        # Backstage catalog entry
├── README.md                # With "Open in Codespaces" button
└── ...                      # Template-specific files
```

### README Badge
Add to each scaffolded README.md:
```markdown
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/${{ values.repoUrl }}?quickstart=1)
```

---

## 4. Golden Path → devcontainer Mapping

| Golden Path | devcontainer Type | Base Image | Key Tools |
|-------------|-------------------|------------|-----------|
| new-microservice | Python | python:3.11 | FastAPI, pytest, uvicorn |
| web-application | Node.js | node:20 | Vite, ESLint, Playwright |
| api-microservice | Python | python:3.11 | FastAPI, SQLAlchemy, Alembic |
| api-gateway | Node.js | node:20 | Express, NGINX config |
| batch-job | Python | python:3.11 | Celery, Redis client |
| data-pipeline | Data | python:3.11 | PySpark, Azure Data SDK |
| event-driven-microservice | Python | python:3.11 | Kafka client, asyncio |
| microservice | Python | python:3.11 | FastAPI, Docker |
| infrastructure-provisioning | Terraform | base:ubuntu | Terraform, az cli, tfsec |
| basic-cicd | Terraform | base:ubuntu | GitHub Actions, Docker |
| security-baseline | Terraform | base:ubuntu | tfsec, Trivy, OPA |
| documentation-site | Node.js | node:20 | MkDocs, techdocs-core |
| gitops-deployment | Terraform | base:ubuntu | ArgoCD CLI, Helm, kubectl |
| rag-application | AI/ML | python:3.11 | Azure AI SDK, LangChain |
| foundry-agent | AI/ML | python:3.11 | Azure AI Foundry SDK |
| mlops-pipeline | AI/ML | python:3.11 | MLflow, Azure ML SDK |
| copilot-extension | Node.js | node:20 | TypeScript, Octokit |
| multi-agent-system | AI/ML | python:3.11 | Semantic Kernel, AutoGen |
| sre-agent-integration | AI/ML | python:3.11 | Azure Monitor SDK |
| ado-to-github-migration | Node.js | node:20 | GitHub CLI, az devops |
| reusable-workflows | Terraform | base:ubuntu | GitHub Actions |
