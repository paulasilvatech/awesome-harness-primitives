# Troubleshooting Local RHDH

Common issues and debugging patterns for local RHDH development.
See `scripts/NOTICE` for attribution.

<comparative_testing>

## Baseline vs Customized Debugging

The most effective debugging pattern is **comparative testing**: isolate whether an issue is in your customizations or in RHDH itself.

```bash
# 1. Stop and switch to pristine
rhdh local down
rhdh local up --baseline

# 2. Test at http://localhost:7007
# If it works → issue is in your customizations
# If it doesn't → issue is in RHDH itself (or rhdh-local)

# 3. Restore customized mode
rhdh local down && rhdh local up --customized
```

| Symptom | Works in Baseline? | Root Cause |
|---------|-------------------|------------|
| Plugin not loading | Yes | Check `dynamic-plugins.override.yaml` - wrong package ref or missing `disabled: false` |
| Plugin not loading | No | Plugin may be incompatible with this RHDH version |
| 504 Gateway Timeout | Yes | Customization broke network namespace - check `compose.override.yaml` |
| 504 Gateway Timeout | No | Lightspeed/Orchestrator network namespace issue - restart all containers together |
| Auth failures | Yes | Check `AUTH_GITHUB_CLIENT_ID` and `AUTH_GITHUB_CLIENT_SECRET` in `.env` |
| Missing catalog entities | Yes | Check `catalog-entities/*.override.yaml` formatting |

</comparative_testing>

<common_errors>

## Common Error Patterns

### 504 Gateway Timeout with Lightspeed

**Cause:** Lightspeed and RHDH share a network namespace. Restarting one container independently desynchronizes the network, causing 504 errors.

**Fix:** Always use `rhdh local down && rhdh local up` instead of restarting individual services with `podman compose restart`. Stopping and starting the entire compose project together keeps the shared network namespace in sync.

### Plugin Install Failures

**Symptoms:** `install-dynamic-plugins` container exits with errors.

**Debug:**

```bash
cd rhdh-local-setup/rhdh-local
podman compose logs install-dynamic-plugins
```

**Common causes:**

- Invalid OCI reference in `dynamic-plugins.override.yaml`
- Network issues pulling plugin images
- Version mismatch between plugin and RHDH

### RHDH Startup Crashes

**Debug:**

```bash
cd rhdh-local-setup/rhdh-local
podman compose logs rhdh 2>&1 | tail -100
podman compose logs rhdh 2>&1 | grep -i error
```

**Common causes:**

- Invalid `app-config.local.yaml` syntax (YAML indentation)
- Missing required environment variables
- Plugin configuration errors in `app-config`

### Database Connection Issues

**Symptoms:** RHDH logs show `ECONNREFUSED` to PostgreSQL.

**Fix:** Ensure `db` service is running and healthy:

```bash
podman compose ps db
podman compose logs db
```

If using `--volumes` on `rhdh local down`, the database is wiped - this is expected.

</common_errors>

<health_checks>

## Health Check Commands

```bash
# Full health check
rhdh local health

# Manual checks
curl http://localhost:7007/api/catalog/health    # Catalog backend
curl http://localhost:7007                        # Frontend
```

### What `rhdh local health` Checks

1. **Container runtime** - podman/docker available
2. **Port 7007** - RHDH accessible
3. **Container status** - all compose services running
4. **Backend health** - catalog API responding

</health_checks>

<update_workflow>

## Updating rhdh-local from Upstream

```bash
# 1. Stop
rhdh local down

# 2. Pull upstream changes
cd rhdh-local-setup/rhdh-local && git pull && cd ../..

# 3. Start pristine to verify update works
rhdh local up --baseline

# 4. If pristine works, switch to customized
rhdh local down && rhdh local up --customized

# 5. Check for deprecation warnings
cd rhdh-local-setup/rhdh-local && podman compose logs rhdh 2>&1 | grep -i deprecat
```

</update_workflow>
