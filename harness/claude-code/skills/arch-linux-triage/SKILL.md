---
name: arch-linux-triage
description: >-
  Diagnose and remediate Arch Linux incidents with pacman, systemd, journal analysis,
  rolling-release upgrade discipline, kernel awareness, and rollback practices. Use when the user
  asks to triage Arch service failures, package conflicts, broken upgrades, boot issues, or
  post-update regressions.
---

<!-- Generated from harness/github-copilot/skills/arch-linux-triage/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Arch Linux triage

Diagnose an Arch Linux problem report, transform update and constraint details into a rolling-release-safe triage plan, and return copy-paste-ready remediation, validation, and rollback commands.

## When to invoke

- "Triage this Arch Linux failure."
- "Fix a pacman or broken upgrade problem."
- "Debug an Arch service after a recent update."
- "Why did my Arch kernel update break boot or drivers?"
- "Give me Arch remediation commands with rollback."

## Request facts to capture

Preserve these original inputs when they are supplied by the caller: `${input:ArchSnapshot}`, `${input:ProblemSummary}`, and `${input:Constraints}`. If any are absent, collect equivalent evidence with read-only commands.

| Fact | How to collect | Why it matters |
| --- | --- | --- |
| Recent update set | `grep -E "\[ALPM\] (upgraded|installed|removed)" /var/log/pacman.log | tail -50` | Arch failures often follow a partial or recent upgrade. |
| Kernel/runtime match | `uname -r`; `pacman -Q linux linux-lts 2>/dev/null`; `bootctl status` when systemd-boot is used | Drivers fail when the running kernel and installed modules do not match. |
| Package health | `pacman -Qk`; `pacman -Dk`; `pacman -Qu` | Finds missing files, dependency issues, and pending upgrades. |
| Failing unit | `systemctl status <unit> --no-pager`; `journalctl -u <unit> -b --no-pager` | Identifies service, dependency, and configuration failures. |
| Constraints | no reboot, no full upgrade, metered network, production host | Determines whether a full `pacman -Syu`, reboot, or package cache rollback is acceptable. |

A step-by-step triage plan should still stay small enough to validate after each major command.

## Triage command map

| Symptom | First commands | Evidence to read |
| --- | --- | --- |
| Service failed | `systemctl status <unit> --no-pager`; `journalctl -u <unit> -b --no-pager` | Exit status, missing library, config parse error, dependency failure. |
| Broken upgrade | `pacman -Syu`; `pacman -Qkk <package>`; `pacman -Dk` | Partial upgrade, interrupted transaction, missing files, dependency drift. |
| Boot regression | `journalctl -b -1 -p warning --no-pager`; `ls /boot`; `mkinitcpio -P` after config review | initramfs, bootloader entry, kernel/module mismatch. |
| Network/DNS | `ip link`; `ip addr`; `ip route`; `resolvectl status`; `networkctl status` | Interface down, route missing, resolver issue, NetworkManager/systemd-networkd mismatch. |
| Pacman lock | `fuser /var/lib/pacman/db.lck`; inspect running pacman processes | Active transaction versus stale lock. |
| AUR-related issue | Identify AUR packages with `pacman -Qm` | AUR rebuilds may be needed after library soname updates. |

## Remediation patterns

| Problem | Preferred fix | Avoid |
| --- | --- | --- |
| Partial upgrade | Bring the system forward with `pacman -Syu` from a healthy mirror. | Installing one package with `pacman -Sy <pkg>` without full upgrade. |
| Broken package files | Reinstall the package: `pacman -S <package>` after confirming the database is healthy. | Manually copying files into `/usr`. |
| Kernel module mismatch | Reboot into the installed kernel, or install matching kernel/modules and regenerate initramfs with `mkinitcpio -P`. | Loading modules built for a different kernel. |
| Mirror failure | Refresh mirror list with a trusted method, then `pacman -Syyu` only when mirror metadata is suspect. | Repeated `-Syy` as routine maintenance. |
| Stale lock | Remove `/var/lib/pacman/db.lck` only after confirming no pacman process owns it. | Deleting the lock while pacman is running. |
| AUR rebuild needed | Rebuild affected foreign packages after core library upgrades. | Treating AUR packages as officially supported pacman packages. |

## Rolling-release safety rules

- Treat partial upgrades as unsupported; prefer a coherent full-system update when package state is involved.
- Read Arch News before major manual interventions when core packages, kernels, Python, OpenSSL, or filesystem layout changed recently.
- Keep rollback grounded in the package cache under `/var/cache/pacman/pkg/` or a known snapshot from the user's environment.
- Include reboot guidance whenever kernel, initramfs, graphics driver, systemd, glibc, or low-level libraries changed.

## Output template

````markdown
## Arch Linux triage result

**Status:** diagnosed | remediated | blocked
**Snapshot/update context:** `<ArchSnapshot or collected evidence>`
**Problem:** `<ProblemSummary>`
**Constraints:** `<Constraints or none stated>`

### Summary
<one-paragraph diagnosis and risk statement>

### Triage Steps
1. `<read-only command>` — <evidence expected>
2. `<read-only command>` — <evidence expected>

### Remediation Commands
```bash
# precheck
<command>
# change
<command>
```

### Validation
```bash
<command proving the fix>
```

### Rollback/Cleanup
- **Rollback/Cleanup**
```bash
<command to undo, downgrade, reboot, or clean up>
```
````

## Quality gate

- [ ] `${input:ArchSnapshot}`, `${input:ProblemSummary}`, and `${input:Constraints}` were used or marked unknown.
- [ ] Recent updates and environment assumptions were checked before remediation.
- [ ] Triage used `systemctl`, `journalctl`, and `pacman` where applicable.
- [ ] Kernel update, initramfs, module, or reboot considerations were addressed when relevant.
- [ ] Every major change includes validation and rollback or cleanup commands.
- [ ] No partial-upgrade remediation was recommended without calling out the risk.
