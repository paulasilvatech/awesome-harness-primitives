# Troubleshooting reference

## Troubleshooting

### Terraform init fails

```bash
# Clear the provider cache but keep .terraform.lock.hcl — deleting it drops the
# pinned provider set and can pull a breaking major version.
rm -rf terraform/.terraform
terraform init
```

### Terraform plan fails with variable errors

```bash
# Verify all required vars are set
./scripts/validate-config.sh --environment <env>
```

### AKS cluster unreachable

```bash
# Refresh credentials
az aks get-credentials --resource-group <rg> --name <cluster> --overwrite-existing
kubectl get nodes
```

### ArgoCD not starting

```bash
kubectl get pods -n argocd
kubectl describe pod -n argocd -l app.kubernetes.io/name=argocd-server
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-server
```

