# Deployment modes reference

## Environment Configurations

| Environment | Mode | Estimated Cost | Features |
|-------------|------|----------------|----------|
| dev | express | $50-100/month | Minimal: AKS + ACR + ArgoCD + Observability |
| staging | standard | $500-1000/month | Production-like: + Databases + ESO + Defender + AI |
| prod | enterprise | $3000+/month | Full HA: + DR + Purview + Runners + Backstage + Cost Mgmt |

## Deployment Modes

| Mode | Nodes | HA | GPU | Best For |
|------|-------|----|-----|----------|
| express | 3 × D4s | No | No | Development, testing |
| standard | 5 × D4s | Yes | No | Production workloads |
| enterprise | 10 × D8s + workload pool | Yes (3 zones) | Optional | Enterprise, multi-tenant |
