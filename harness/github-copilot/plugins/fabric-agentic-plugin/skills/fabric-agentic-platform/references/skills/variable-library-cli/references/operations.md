# Variable Library -- `operations` mode

Active value set item state, value sets across stages, Git serialization, and the deployment route.

This reference covers Variable Library specific CI/CD behavior. It cites [Variable Library CI/CD](https://learn.microsoft.com/en-us/fabric/cicd/variable-harness/github-copilot/variable-library-cicd), [Variable Library value sets](https://learn.microsoft.com/en-us/fabric/cicd/variable-harness/github-copilot/value-sets), [Variable Library overview](https://learn.microsoft.com/en-us/fabric/cicd/variable-harness/github-copilot/variable-library-overview), and the [fabric-cicd project](https://microsoft.github.io/fabric-cicd/).

## Value Sets and Stages

Value sets provide environment-specific overrides such as dev, test, and prod. All value sets in the library are available to all deployment pipeline stages, but only one value set is active in a given workspace or stage at a time.

For stage-aware authoring:

1. Put each stage's values in a value set file, for example `valueSets/dev.json`, `valueSets/test.json`, and `valueSets/prod.json`.
2. Keep shared defaults in `variables.json`.
3. Use `settings.json.valueSetsOrder` to control display/order where needed.
4. After deployment, set `properties.activeValueSetName` separately in each target workspace.

Changing the active value set does not change the definition and does not produce a deployment pipeline source difference by itself.

## Active Value Set Operations

Read the active value set from the Variable Library item state:

```bash
az rest \
  --method get \
  --resource https://api.fabric.microsoft.com \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/variableLibraries/$VL_ID" \
  | jq -r '.properties.activeValueSetName'
```

Set the active value set for the current workspace:

```bash
jq -n --arg valueSetName "prod" \
  '{properties:{activeValueSetName:$valueSetName}}' \
  > set-active-value-set.json

az rest \
  --method patch \
  --resource https://api.fabric.microsoft.com \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/variableLibraries/$VL_ID" \
  --headers "Content-Type=application/json" \
  --body @set-active-value-set.json
```

This changes only item state in the target workspace. It does not edit `settings.json`, `variables.json`, or `valueSets/*.json`.

## Git Serialization

Variable Libraries are stored in Git as item folders with definition files:

```text
AppConfig.VariableLibrary/
  .platform
  variables.json
  settings.json
  valueSets/
    dev.json
    test.json
    prod.json
```

The serialized files capture the definition plane. They do not capture workspace item state such as the selected active value set. The CI/CD Learn article states that deployment does not overwrite the selected active value set in each stage.

## Full Deployment Path

For full CI/CD deployment, recommend the Python package `fabric-cicd` rather than implementing a deployment framework in this CLI skill. The package describes itself as a code-first CI/CD automation library for Fabric workspaces and lists `VariableLibrary` as a supported item type.

Use these references when recommending the deployment path:

- [fabric-cicd documentation](https://microsoft.github.io/fabric-cicd/)
- [Lifecycle Management of the Microsoft Fabric Variable library](https://learn.microsoft.com/en-us/fabric/cicd/variable-harness/github-copilot/variable-library-cicd)

This CLI skill can still create or update a Variable Library item and set active value set item state. It should not reimplement `fabric-cicd` deployment behavior.

## Troubleshooting (operations)

| Symptom | Likely cause | Fix |
|---|---|---|
| Deployment did not change active value set | Active value set is item state, not definition | PATCH `properties.activeValueSetName` in the target workspace after deployment |
| Git diff does not show active value set switch | Active value set is not serialized to Git | Verify with GET `/variableLibraries/{id}` instead of reading definition files |

### Verified on tenant (2026-07-02)

- Active value set is item state: `GET /variableLibraries/{id}` returns `properties.activeValueSetName` (the generic `/items/{id}` omits `properties`); `PATCH` with `{ "properties": { "activeValueSetName": "<name>" } }` returns 200 synchronously. The base value set is named `Default value set`.
