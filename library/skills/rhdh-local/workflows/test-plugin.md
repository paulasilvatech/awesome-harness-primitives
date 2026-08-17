# Workflow: Test a Plugin End-to-End in Local RHDH

<required_reading>

- `../overlay/references/rhdh-local.md` section `<test_entities>` - catalog entity template and annotation patterns
- `../overlay/references/rhdh-local.md` section `<dynamic_plugins_config>` - plugin YAML format
- `../overlay/references/rhdh-local.md` section `<verification_checklist>` - what to verify
- `../overlay/references/rhdh-local.md` section `<extensions_catalog_visibility>` - optional Extensions Catalog setup
- `references/troubleshooting.md` - comparative testing and common error patterns
</required_reading>

<process>
## Step 1: Ensure Plugin is Enabled

Verify the plugin is enabled in `rhdh-customizations/configs/dynamic-plugins/dynamic-plugins.override.yaml` with `disabled: false`. If not, run the `enable-plugin.md` workflow first.

---

## Step 2: Create a Test Catalog Entity

Edit `rhdh-customizations/configs/catalog-entities/components.override.yaml`:

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: <plugin>-test-service
  description: Test entity for <plugin> plugin verification
  annotations:
    # Add the annotation(s) required by the plugin
    <annotation-key>: <test-value>
spec:
  type: service
  lifecycle: experimental
  owner: user:default/guest
```

Find the required annotation from the plugin's `spec.appConfigExamples` or the plugin's README in the overlay repo.

**Common annotation patterns:**

| Plugin Family | Annotation Key | Example Value |
|---------------|----------------|---------------|
| AWS CodePipeline | `aws.amazon.com/aws-codepipeline-arn` | `arn:aws:codepipeline:us-east-1:000000000000:test` |
| ArgoCD | `argocd/app-name` | `<app-name>` |
| Tekton | `janus-idp.io/tekton` | `<namespace>` |
| Kubernetes | `backstage.io/kubernetes-id` | `<service-name>` |

---

## Step 3: Apply and Restart

```bash
rhdh local apply
rhdh local down && rhdh local up --customized [--lightspeed|--orchestrator|--both]
```

---

## Step 4: Watch Logs During Startup

```bash
cd rhdh-local
podman compose logs install-dynamic-plugins     # Wait for "Done" or errors
podman compose logs rhdh 2>&1 | tail -100       # Watch for startup errors
podman compose logs rhdh 2>&1 | grep -i <plugin>  # Plugin-specific messages
```

---

## Step 5: Verify in the UI

1. Open `http://localhost:7007` - Login as Guest
2. Navigate to **Catalog** and find the test entity (`<plugin>-test-service`)
3. Open the entity's **Overview** tab
4. Verify the plugin card renders (error messages about missing credentials are OK - the card rendering itself is what matters)

---

## Step 6: Check Backend Health (if backend plugin)

```bash
curl http://localhost:7007/api/<plugin>/health
# Expected: {"status":"ok"}
```

---

## Step 7: Extensions Catalog (Optional)

To see the plugin in the Extensions Catalog at `/extensions/catalog`, follow the setup in:
`../overlay/references/rhdh-local.md` section `<extensions_catalog_visibility>`

---

## Step 8: Cleanup After Testing

If this was a temporary test (e.g. for a PR review), remove customizations:

```bash
rhdh local remove --force
```

This removes all copied override files from `rhdh-local/` without touching `rhdh-customizations/` source files.

> **Note:** Do not delete files directly from `rhdh-local/` - always use `rhdh local remove` to keep the copy-sync invariant intact.

</process>

<success_criteria>
**Plugin loads correctly:**

- [ ] No errors in `podman compose logs install-dynamic-plugins`
- [ ] No plugin-related errors in `podman compose logs rhdh`
- [ ] Backend health endpoint returns `{"status":"ok"}` (if backend plugin)

**Entity card works:**

- [ ] Test entity visible in catalog at `/catalog`
- [ ] Plugin card renders on entity Overview tab
- [ ] Card shows expected content (errors about missing credentials are acceptable)

**Extensions Catalog (optional):**

- [ ] Plugin appears in `/extensions/catalog`
- [ ] Plugin name, description, categories display correctly
</success_criteria>
