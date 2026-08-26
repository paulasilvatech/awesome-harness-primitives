# Mainframe modernization migration snapshot

This subtree is the source snapshot used to migrate the SIFAP workshop customizations into the governed
GitHub Copilot harness. It is retained for comparison and traceability; it is not the canonical source for
active primitives.

## Canonical package

The maintained package is
[`harness/github-copilot/plugins/mainframe-modernization/`](../harness/github-copilot/plugins/mainframe-modernization/).
It contains four stage agents, SIFAP context and traceability Skills, focused instructions and prompts,
shared generated Skills, and the transactional `sifap-workspace-kit` publisher.

Do not update the snapshot's old agents, prompts, instructions, empty skill directories, or local plugin
manifests independently. Make changes in the canonical package and use its workspace kit to publish a
clean target repository.

## Publication

After installing `mainframe-modernization@copilot-primitives`, preview a target repository with:

```bash
python3 scripts/install_workspace_kit.py \
  --target <repository> \
  --profile full
```

Run the same command with `--apply` only after reviewing the preview. Project copies are managed outputs,
not a second source of truth.

## References

- [Canonical plugin](../harness/github-copilot/plugins/mainframe-modernization/README.md)
- [Harness contract](../docs/COPILOT-HARNESS-SPEC.md)
- [Runtime evidence](../docs/HARNESS-VALIDATION.md#mainframe-modernization-plugin-runtime-verification)
