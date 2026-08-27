---
name: fedora-linux-triage
description: >-
  Diagnose and remediate Fedora Linux incidents with dnf, systemd, journal analysis, SELinux,
  firewalld, release-upgrade awareness, and rollback practices. Use when the user asks to triage
  Fedora service failures, package issues, boot problems, network/firewall symptoms, or SELinux
  denials.
---

<!-- Generated from harness/github-copilot/skills/fedora-linux-triage/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Fedora Linux triage

Diagnose a Fedora problem report, transform release and constraint details into a Fedora-appropriate triage plan, and return copy-paste-ready remediation, validation, and rollback commands.

## When to invoke

- "Triage this Fedora service failure."
- "Fix a Fedora dnf package problem."
- "Why is SELinux blocking this on Fedora?"
- "Debug Fedora firewalld or networking."
- "Give me Fedora remediation commands with rollback."

## Request facts to capture

Preserve these original inputs when they are supplied by the caller: `${input:FedoraRelease}`, `${input:ProblemSummary}`, and `${input:Constraints}`. If they are absent, collect equivalent facts before changing the system.

| Fact | How to collect | Why it matters |
| --- | --- | --- |
| Release | `cat /etc/fedora-release`; `cat /etc/os-release`; `rpm -E %fedora` | Fedora changes quickly; release age affects repositories and upgrade path. |
| Package history | `dnf history list`; `dnf history info last`; `rpm -qa --last | head` | Recent upgrades, removals, and repo changes explain many failures. |
| Failing unit | `systemctl status <unit> --no-pager`; `journalctl -u <unit> -b --no-pager` | Shows service exit code, dependency failure, port conflict, or policy denial. |
| Security state | `getenforce`; `ausearch -m AVC,USER_AVC -ts recent` | SELinux denials are common and should be fixed narrowly. |
| Firewall state | `firewall-cmd --state`; `firewall-cmd --list-all`; `firewall-cmd --get-active-zones` | firewalld runtime/permanent mismatches are common. |
| Constraints | no reboot, no upgrade, production host, offline host | Determines whether to restart, reboot, downgrade, or only gather evidence. |

A step-by-step triage plan should still stay conservative and reversible.

## Triage command map

| Symptom | First commands | Evidence to read |
| --- | --- | --- |
| Service failed | `systemctl status <unit> --no-pager`; `journalctl -u <unit> -b --no-pager` | Exit status, config parse failure, denied resource, missing dependency. |
| DNF issue | `dnf check`; `dnf repolist`; `dnf history list`; `dnf repoquery --unsatisfied` | Broken deps, disabled repos, third-party repo drift. |
| SELinux denial | `getenforce`; `ausearch -m AVC,USER_AVC -ts recent`; `sealert -a /var/log/audit/audit.log` if available | Denied class, source context, target path, suggested boolean or labeling fix. |
| firewalld block | `firewall-cmd --list-all`; `ss -tulpn`; external connection test | Service listening versus firewall exposure. |
| Boot/kernel issue | `journalctl -b -p warning --no-pager`; `uname -r`; `rpm -q kernel-core` | Kernel mismatch, initramfs, driver, failed mount. |
| Release upgrade residue | `dnf system-upgrade log --number=-1`; `dnf distro-sync` planning | Incomplete upgrade or package set drift. |

## Remediation patterns

| Problem | Preferred fix | Avoid |
| --- | --- | --- |
| Failed service after config change | Run daemon config validation, then `systemctl restart <unit>` and inspect status. | Restarting repeatedly without reading journal evidence. |
| Package drift | Use `dnf distro-sync` after reviewing the transaction; use `dnf history undo <ID>` for specific reversible changes. | Mixing incompatible third-party repos without pinning or review. |
| SELinux label issue | `restorecon -Rv <path>` or correct file context with `semanage fcontext` then `restorecon`. | Permanent `setenforce 0`. |
| SELinux boolean needed | `getsebool -a | grep <topic>` then `setsebool -P <boolean> on` only when it matches the service design. | Generating broad local policy before checking booleans and labels. |
| firewalld rule missing | Test with runtime `firewall-cmd --add-service=<service>`, validate, then apply `--permanent` and `--reload`. | Editing nftables/iptables behind firewalld. |
| Kernel update pending | Validate installed kernels and reboot into the target kernel when constraints allow. | Troubleshooting drivers against an old running kernel after updating packages. |

## Safety rules

- Prefer read-only evidence before package, firewall, SELinux, or boot changes.
- Treat SELinux as part of the diagnosis, not an obstacle to disable; fix labels, booleans, or narrow policy.
- Call out reboot requirements for kernel, glibc, systemd, firmware, and driver updates.
- Include rollback through `dnf history undo`, config backup restore, firewalld runtime removal, or SELinux context reversal where possible.

## Output template

````markdown
## Fedora triage result

**Status:** diagnosed | remediated | blocked
**Release:** `<FedoraRelease or collected release>`
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

- [ ] `${input:FedoraRelease}`, `${input:ProblemSummary}`, and `${input:Constraints}` were used or marked unknown.
- [ ] Release and environment assumptions were confirmed before remediation.
- [ ] Triage used `systemctl`, `journalctl`, and `dnf` where applicable.
- [ ] SELinux and `firewalld` were considered when symptoms involve access, ports, or policy.
- [ ] Every major change includes validation and rollback or cleanup commands.
- [ ] Commands are copy-paste-ready and avoid destructive action without a precheck.
