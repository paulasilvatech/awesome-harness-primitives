# Mainframe modernization migration snapshot

This subtree is the source snapshot used to migrate the SIFAP workshop customizations into the governed
GitHub Copilot harness. It is retained for comparison and traceability; it is not the canonical source for
active primitives.

## Canonical package

The maintained package is
[`harness/github-copilot/plugins/mainframe-natural-adabas/`](../../../harness/github-copilot/plugins/mainframe-natural-adabas/).
It contains five stage agents, SIFAP context and traceability Skills, the loop and engineering graph,
focused instructions and prompts, shared generated Skills, and the transactional
`modernization-workspace-kit`
publisher. COBOL and DB2 systems use the sibling `mainframe-cobol-db2` package.

Do not update the snapshot's old agents, prompts, instructions, empty skill directories, or local plugin
manifests independently. Make changes in the canonical package and use its workspace kit to publish a
clean target repository.

## Publication

After installing `mainframe-natural-adabas@copilot-primitives`, preview a target repository with:

```bash
python3 scripts/install_workspace_kit.py \
  --target <repository> \
  --profile full
```

Run the same command with `--apply` only after reviewing the preview. Project copies are managed outputs,
not a second source of truth.

## References

- [Canonical plugin](../../../harness/github-copilot/plugins/mainframe-natural-adabas/README.md)
- [Harness contract](../../COPILOT-HARNESS-SPEC.md)
- [Runtime evidence](../../HARNESS-VALIDATION.md#mainframe-modernization-plugin-runtime-verification)
