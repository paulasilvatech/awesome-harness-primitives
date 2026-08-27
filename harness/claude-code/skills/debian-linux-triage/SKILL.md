---
name: debian-linux-triage
description: >-
  Diagnose and remediate Debian Linux incidents with apt, dpkg, systemd, journal analysis,
  AppArmor-aware checks, firewall review, and rollback practices. Use when the user asks to triage
  Debian service failures, package issues, boot problems, network symptoms, or security-profile
  denials.
---

<!-- Generated from harness/github-copilot/skills/debian-linux-triage/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Debian Linux triage

Diagnose a Debian problem report, transform release and constraint details into a conservative apt/dpkg triage plan, and return copy-paste-ready remediation, validation, and rollback commands.

## When to invoke

- "Triage this Debian service failure."
- "Fix a Debian apt or dpkg problem."
- "Why is AppArmor blocking this process on Debian?"
- "Debug networking or firewall behavior on Debian."
- "Give me Debian remediation commands with rollback."

## Request facts to capture

Preserve these original inputs when they are supplied by the caller: `${input:DebianRelease}`, `${input:ProblemSummary}`, and `${input:Constraints}`. Ask concise follow-ups only when the missing fact changes the safety of the fix.

| Fact | How to collect | Why it matters |
| --- | --- | --- |
| Release | `cat /etc/debian_version`; `cat /etc/os-release`; `lsb_release -a 2>/dev/null` | Stable, testing, and oldstable differ in repositories and support. |
| Package state | `apt-cache policy <package>`; `dpkg -l | grep '^..r'`; `sudo dpkg --audit` | Finds held, half-configured, removed-but-configured, and dependency-broken packages. |
| Failing unit | `systemctl status <unit> --no-pager`; `journalctl -u <unit> -b --no-pager` | Distinguishes service, dependency, config, and permission failures. |
| Security profile | `aa-status`; `journalctl -k -g DENIED --no-pager` | AppArmor denials can look like application bugs. |
| Firewall | `nft list ruleset`; `ufw status verbose` when UFW is installed | Debian hosts may use nftables directly or UFW as a frontend. |
| Constraints | no reboot, pinned packages, production host, no network | Determines whether to restart, reinstall, unhold, or only gather evidence. |

A step-by-step triage plan should still stay conservative and reversible.

## Triage command map

| Symptom | First commands | Evidence to read |
| --- | --- | --- |
| Service failed | `systemctl status <unit> --no-pager`; `journalctl -u <unit> -b --no-pager` | Exit code, config parse error, dependency, denied file or port. |
| Apt failure | `sudo apt update`; `sudo apt -f install`; `sudo dpkg --configure -a` after reading the error | Repository mismatch, held package, interrupted configure step. |
| Package ownership | `dpkg -S <path>`; `dpkg -L <package>` | Confirms which package owns or should provide a file. |
| Boot issue | `journalctl -b -p warning --no-pager`; `systemctl --failed`; `findmnt --verify` | Failed mounts, missing firmware, unit ordering. |
| Network path | `ip addr`; `ip route`; `resolvectl status`; `ss -tulpn` | Addressing, routing, resolver, listener. |
| AppArmor denial | `aa-status`; `journalctl -k --since -1h | grep -i apparmor` | Profile enforce/complain mode and denied operation. |

## Remediation patterns

| Problem | Preferred fix | Avoid |
| --- | --- | --- |
| Interrupted package configuration | `sudo dpkg --configure -a`, then `sudo apt -f install` if dependencies remain broken. | Removing `/var/lib/dpkg/` metadata. |
| Wrong or missing package | `sudo apt install --reinstall <package>` after checking `apt-cache policy`. | Installing random `.deb` files without source and dependency review. |
| Held package blocks upgrade | `apt-mark showhold`; unhold only the intended package with `sudo apt-mark unhold <package>`. | Blanket unhold of all packages. |
| AppArmor false block | Switch a specific profile to complain mode for diagnosis with `aa-complain <profile>`, then update policy or restore enforce mode. | Disabling AppArmor globally as a permanent fix. |
| Firewall missing port | Add a narrow UFW/nftables rule and verify with `ss -tulpn` plus an external connection test. | Opening broad port ranges without a service reason. |
| Service config error | Run the daemon's config test before restart, then `systemctl restart <unit>`. | Editing and restarting without syntax validation. |

## Safety rules

- Prefer `apt` for interactive remediation and `apt-get` for scripts; use `dpkg` only for package database operations that apt cannot complete.
- Check `/etc/apt/sources.list` and `/etc/apt/sources.list.d/*.list` before changing repository-related failures.
- Include reboot guidance when kernel, libc, systemd, firmware, or low-level security components changed.
- Keep rollback realistic: package reinstall, config backup restore, `apt-mark hold`, or service restart; do not promise impossible downgrades without available repositories.

## Output template

````markdown
## Debian triage result

**Status:** diagnosed | remediated | blocked
**Release:** `<DebianRelease or collected release>`
**Problem:** `<ProblemSummary>`
**Constraints:** `<Constraints or none stated>`

### Summary
<one-paragraph diagnosis and risk statement>

### Triage Steps
1. `<read-only command>` — <evidence expected>
2. `<read-only command>` — <evidence expected>

### Remediation Commands
```bash
# backup or precheck
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
<command to undo or clean up>
```
````

## Quality gate

- [ ] `${input:DebianRelease}`, `${input:ProblemSummary}`, and `${input:Constraints}` were used or marked unknown.
- [ ] Release and environment assumptions were confirmed before remediation.
- [ ] Triage used `systemctl`, `journalctl`, `apt`, and `dpkg` where applicable.
- [ ] AppArmor or firewall considerations were addressed when symptoms involve access, ports, or policy.
- [ ] Every major change includes validation and rollback or cleanup commands.
- [ ] Commands are copy-paste-ready and avoid destructive package database changes.
