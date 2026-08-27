# Rollback reference

## Rollback

### Rollback H3 only
```bash
# Disable AI Foundry
# Set enable_ai_foundry = false in tfvars
terraform plan -var-file=environments/<env>.tfvars -out=rollback.tfplan
terraform apply rollback.tfplan
```

### Complete teardown
```bash
./scripts/deploy-full.sh --environment <env> --destroy
```
