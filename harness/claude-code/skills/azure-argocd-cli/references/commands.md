# ArgoCD CLI command reference

## Installation & Bootstrap

### 1. Install ArgoCD via Helm
```bash
# Add ArgoCD Helm repo
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# Create namespace
kubectl create namespace argocd

# Install with project values
helm install argocd argo/argo-cd \
  --namespace argocd \
  --values deploy/helm/argocd/values.yaml \
  --wait --timeout 10m

# Verify installation
kubectl get pods -n argocd
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s
```

### 2. Get Initial Admin Password
```bash
# Get auto-generated admin password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d; echo

# Login via CLI
argocd login argocd.${DNS_ZONE_NAME} --username admin --password <password>
```

### 3. Configure Repository Credentials
```bash
# Apply repository credentials from manifests
kubectl apply -f argocd/repo-credentials.yaml

# Or add via CLI
argocd repo add https://github.com/${GITHUB_ORG}/open-horizons-platform.git \
  --username <username> --password <github-token>

# Verify
argocd repo list
```

### 4. Bootstrap App-of-Apps
```bash
# Apply root application (bootstraps all child apps)
kubectl apply -f argocd/app-of-apps/root-application.yaml

# Apply sync policies
kubectl apply -f argocd/sync-policies.yaml

# Verify apps are created
argocd app list
```

### 5. Configure External Secrets Integration
```bash
# Apply cluster secret store
kubectl apply -f argocd/secrets/cluster-secret-store.yaml

# Deploy External Secrets app
kubectl apply -f argocd/apps/external-secrets.yaml

# Deploy Gatekeeper
kubectl apply -f argocd/apps/gatekeeper.yaml
```

## Day-2 Operations

### Authentication
```bash
# Login to ArgoCD
argocd login <ARGOCD_SERVER> --username admin --password <password>

# Current context
argocd context
```

### Application Operations
```bash
# List applications
argocd app list

# Get application status
argocd app get <app-name>

# Show application diff (ALWAYS do before sync)
argocd app diff <app-name>

# Sync application
argocd app sync <app-name>

# Sync with prune (careful in production)
argocd app sync <app-name> --prune

# Hard refresh
argocd app get <app-name> --hard-refresh
```

### Health & Status
```bash
# Application health
argocd app get <app-name> -o json | jq '.status.health.status'

# Sync status
argocd app get <app-name> -o json | jq '.status.sync.status'

# Resources status
argocd app resources <app-name>
```

### Troubleshooting
```bash
# Check ArgoCD server logs
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-server --tail=100

# Check application controller logs
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller --tail=100

# Check repo server logs
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-repo-server --tail=100

# Force sync
argocd app sync <app-name> --force

# Check events
kubectl get events -n argocd --sort-by='.lastTimestamp'
```

## Project Files Reference
- **Helm values:** `deploy/helm/argocd/values.yaml`
- **App-of-apps:** `argocd/app-of-apps/root-application.yaml`
- **Sync policies:** `argocd/sync-policies.yaml`
- **Repo credentials:** `argocd/repo-credentials.yaml`
- **Secret store:** `argocd/secrets/cluster-secret-store.yaml`
- **Terraform module:** `terraform/modules/argocd/`

## Best Practices
1. ALWAYS diff before sync
2. Use --prune carefully in production
3. Verify health after sync
4. Use projects for access control
5. Enable auto-sync only for non-prod environments
6. Configure notifications for sync failures
7. Use sync waves for ordered deployments
