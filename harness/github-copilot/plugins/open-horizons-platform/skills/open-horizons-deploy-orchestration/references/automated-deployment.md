# Automated deployment reference

### Automated deployment

```bash
# Full deployment
./scripts/deploy-full.sh --environment dev

# Dry run (plan only)
./scripts/deploy-full.sh --environment dev --dry-run

# Deploy specific horizon
./scripts/deploy-full.sh --environment dev --horizon h1

# CI/CD mode (no prompts)
./scripts/deploy-full.sh --environment prod --auto-approve

# Resume after failure
./scripts/deploy-full.sh --environment dev --resume

# Destroy
./scripts/deploy-full.sh --environment dev --destroy
```

