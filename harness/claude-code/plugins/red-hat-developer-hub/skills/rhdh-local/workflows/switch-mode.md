# Workflow: Switch Between Customized and Pristine Mode

<required_reading>

- `references/customization-system.md` - what customized vs pristine means
- `references/troubleshooting.md` - use scripts not direct compose commands, network namespace rules
</required_reading>

<process>
> **Primary interface:** Use `rhdh local up`/`rhdh local down` - they handle copy-sync and compose orchestration directly.
> Direct compose commands (`podman compose up/down`) are available as a fallback but skip customization sync.

## Mode Comparison

| Feature | Customized Mode | Pristine Mode |
|---------|----------------|---------------|
| Configuration | Your `rhdh-customizations/` files | RHDH defaults only |
| Authentication | Your GitHub OAuth (if configured) | Guest user only |
| Plugins | Your override plugins | Default plugins only |
| Environment | Your `.env` overrides | `default.env` only |
| Catalog entities | Your override entities | Example entities only |

**When to use Pristine Mode:**

- Isolating whether an issue is in your config or in RHDH itself
- Testing RHDH updates without your customizations interfering
- Creating minimal reproduction cases for bug reports

**When to use Customized Mode:**

- Normal daily development
- Production-like testing
- Demonstrating features to your team

---

## Switch to Pristine Mode

```bash
rhdh local down
rhdh local up --baseline
```

> `rhdh local down` automatically removes customization copies from `rhdh-local/`.
> `rhdh local up --baseline` starts RHDH with default configuration only.

**Direct compose fallback (skips customization sync):**

```bash
cd rhdh-local && podman compose down && podman compose up -d
```

---

## Switch Back to Customized Mode

```bash
rhdh local apply
rhdh local down && rhdh local up --customized [--lightspeed|--orchestrator|--both]
```

**Direct compose fallback:**

```bash
cd rhdh-local && podman compose down && podman compose up -d
```

---

## Check Current Mode

```bash
# Customization copies exist = Customized mode
ls -la rhdh-local/.env
ls -la rhdh-local/configs/app-config/app-config.local.yaml

# Or check git status (should be clean in either mode)
cd rhdh-local && git status
```

---

## Workflow: Troubleshoot Configuration Issues

If something isn't working in your customized setup:

```bash
# 1. Stop and switch to pristine
rhdh local down
rhdh local up --baseline

# 2. Test at http://localhost:7007
# If it works → issue is in your customizations
# If it doesn't → issue is in RHDH itself

# 3. Restore customized mode
rhdh local apply
rhdh local down && rhdh local up --customized [flags]

# 4. Re-enable customizations one at a time to isolate the problem
```

---

## Workflow: Test a RHDH Update

```bash
# 1. Stop
rhdh local down

# 2. Pull upstream changes
cd rhdh-local-setup/rhdh-local && git pull && cd ../..

# 3. Start pristine and verify new version works
rhdh local up --baseline

# 4. Reapply customizations and test
rhdh local apply
rhdh local down && rhdh local up --customized [flags]

# 5. Check for deprecation warnings in logs
cd rhdh-local-setup/rhdh-local && podman compose logs rhdh 2>&1 | grep -i deprecat
```

</process>

<success_criteria>
**Pristine mode:**

- [ ] `rhdh-local/` git status is clean (`git status` shows no modified files)
- [ ] RHDH starts at `http://localhost:7007` with Guest login
- [ ] No custom plugins or config visible

**Customized mode:**

- [ ] `rhdh local apply` ran without errors
- [ ] Override files exist in `rhdh-local/` (e.g. `rhdh-local/.env` exists)
- [ ] RHDH starts with your custom configuration
- [ ] Your plugins and entities are visible
</success_criteria>
