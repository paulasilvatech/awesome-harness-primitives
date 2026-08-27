---
name: centos-linux-triage
description: >-
  Diagnose and remediate CentOS Linux incidents with RHEL-compatible systemd, journal, dnf/yum,
  SELinux, firewalld, and rollback practices. Use when the user asks to triage CentOS service
  failures, package issues, boot problems, networking/firewall symptoms, or security-policy
  denials.
---

<!-- Generated from harness/github-copilot/skills/centos-linux-triage/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# CentOS Linux triage

Diagnose a CentOS problem report, transform release and constraint details into a safe RHEL-compatible triage plan, and return copy-paste-ready remediation, validation, and rollback commands.

## When to invoke

- "Triage this CentOS service failure."
- "Fix a CentOS package or dnf/yum issue."
- "Why is this CentOS host blocked by SELinux or firewalld?"
- "Give me CentOS remediation commands with rollback."
- "Debug this CentOS Stream or legacy CentOS problem."

## Request facts to capture

Preserve these original inputs when they are supplied by the caller: `${input:CentOSVersion}`, `${input:ProblemSummary}`, and `${input:Constraints}`. If any are absent, infer only safe defaults and mark unknowns explicitly.

| Fact | How to collect | Why it matters |
| --- | --- | --- |
| Release line | `cat /etc/centos-release`, `cat /etc/os-release`, `rpm -E %rhel` | CentOS Stream, CentOS Linux 7, and RHEL-compatible rebuilds differ in package sources and support posture. |
| Runtime context | `systemd-detect-virt`, `hostnamectl`, `uname -r` | Containers, VMs, and bare metal expose different service, kernel, and boot behavior. |
| Failing unit | `systemctl status <unit> --no-pager`, `systemctl is-enabled <unit>` | Separates disabled, failed, masked, missing, and dependency-blocked units. |
| Recent changes | `dnf history info last` or `yum history info last`, `rpm -qa --last | head` | Package updates and removals are common root causes. |
| Constraints | maintenance window, no reboot, no package install, production host | Determines whether to restart, reboot, downgrade, or only gather evidence. |

## Triage command map

| Symptom | First commands | Evidence to read |
| --- | --- | --- |
| Service failed | `systemctl status <unit> --no-pager`; `journalctl -u <unit> -b --no-pager` | Exit code, failed dependency, denied path, missing config, port conflict. |
| Boot or kernel issue | `journalctl -b -p warning --no-pager`; `grubby --default-kernel`; `uname -r` | Kernel mismatch, initramfs failure, failed mount, emergency target cause. |
| Package conflict | `dnf check`; `dnf repolist`; `dnf history list`; use `yum` on legacy hosts | Broken dependencies, disabled repos, modular stream conflicts, incomplete transactions. |
| Disk pressure | `df -h`; `du -xh /var | sort -h | tail`; `journalctl --disk-usage` | Full `/`, `/var`, logs, cache, or application data. |
| Network path | `ip addr`; `ip route`; `ss -tulpn`; `resolvectl status` or `/etc/resolv.conf` | Addressing, routing, DNS, listener, local firewall. |
| SELinux denial | `getenforce`; `ausearch -m AVC,USER_AVC -ts recent`; `sealert -a /var/log/audit/audit.log` | Whether denial is real, recent, and tied to the failing service. |
| firewalld block | `firewall-cmd --state`; `firewall-cmd --list-all`; `firewall-cmd --get-active-zones` | Active zone, allowed service/port, runtime versus permanent mismatch. |

## Remediation patterns

| Problem | Preferred fix | Avoid |
| --- | --- | --- |
| Failed service after config edit | Validate config with the daemon-specific checker, then `systemctl restart <unit>` and `systemctl status <unit> --no-pager`. | Blind restart loops without reading `journalctl`. |
| Missing package | `dnf install <package>` or `yum install <package>` after checking enabled repos. | Curl-piping random RPM installers on production hosts. |
| Broken transaction | `dnf history undo <ID>` when safe, or `dnf distro-sync` for repository drift. | Deleting RPM database files. |
| SELinux denial | Restore labels with `restorecon -Rv <path>`, set documented booleans with `setsebool -P <boolean> on`, or create a narrow policy module only after review. | `setenforce 0` as a permanent fix. |
| firewalld port missing | `firewall-cmd --add-service=<service>` for runtime test, then `--permanent` and `--reload` after validation. | Editing iptables rules behind firewalld. |
| Log growth | `journalctl --vacuum-time=7d` or service-specific retention settings. | Removing live log files without restarting/reopening the writer. |

## Safety rules

- Verify every destructive command with a read-only command first: check before changing packages, firewall, SELinux policy, filesystems, or boot entries.
- Prefer reversible changes: runtime `firewall-cmd` before `--permanent`, config backups before edits, `dnf history undo` for package rollback.
- Include a no-reboot path when constraints prohibit reboot, but state when kernel, glibc, or SELinux policy changes require one for full validation.
- Use `dnf` for CentOS Stream and modern CentOS; use `yum` where the host is legacy and `dnf` is unavailable.

## Output template

````markdown
## CentOS triage result

**Status:** diagnosed | remediated | blocked
**Host/release:** `<CentOS release or unknown>`
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

- [ ] `${input:CentOSVersion}`, `${input:ProblemSummary}`, and `${input:Constraints}` were used or marked unknown.
- [ ] Release and environment assumptions were confirmed before remediation.
- [ ] Triage used `systemctl`, `journalctl`, `dnf`/`yum`, and relevant logs where applicable.
- [ ] SELinux and `firewalld` were considered when symptoms involve access, ports, or policy.
- [ ] Every major change includes validation and rollback or cleanup commands.
- [ ] Commands are copy-paste-ready and avoid destructive action without a precheck.
