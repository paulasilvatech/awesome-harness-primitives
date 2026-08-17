---
applyTo: "**"
description: "Enforces CentOS administration conventions for RHEL-compatible package management, repositories, systemd services, firewalld, SELinux, validation, and rollback guidance."
name: "CentOS Administration Conventions"
---

# CentOS Administration Conventions — RHEL-Compatible Operations

These instructions apply when producing guidance, scripts, or documentation for CentOS environments. They are authoritative for CentOS version targeting, RHEL-compatible terminology, package management, repository controls, configuration paths, systemd services, firewalld, SELinux, validation, and rollback expectations; environment-specific production policy wins where it imposes stricter operational controls.

## Platform Alignment

Identify the CentOS version before choosing commands. Distinguish CentOS Stream and legacy CentOS releases because package availability, repositories, and lifecycle expectations differ. Use RHEL-compatible terminology and paths so guidance transfers cleanly to related enterprise Linux environments.

## Package Management and Repositories

Use package tools that match the platform version.

| Platform | Convention |
| --- | --- |
| CentOS Stream and CentOS 8+ (`Stream/8` shorthand) | Prefer `dnf`. |
| CentOS 7 | Use `yum`. |
| Package details | Use `dnf info`, `yum info`, and `dnf repoquery` where available. |
| Version stability | Use `dnf versionlock` or `yum versionlock` when packages must stay fixed. |
| External packages | Call out EPEL dependencies and show how to enable/disable them safely. |
| Repository trust | Verify repositories with GPG checks enabled. |

Avoid mixing `dnf` and `yum` guidance without naming the target release.

## Configuration, Services, and Firewall

Place service environment files in `/etc/sysconfig/` when the service expects that convention. Use systemd drop-ins for overrides and `systemctl` for service control. Prefer `firewalld` with `firewall-cmd` unless the environment explicitly standardizes on `iptables` or `nftables`.

## SELinux, Audit Logs, and Safety

Keep SELinux in enforcing mode whenever possible. Use `semanage`, `restorecon`, and `setsebool` for policy adjustments rather than disabling SELinux. Reference `/var/log/audit/audit.log` when diagnosing denials. Include copy-paste-ready commands, verification steps after changes, and rollback steps for risky operations.

## Good / Bad Examples

The examples below illustrate version-aware package and service guidance.

**Good:**

```bash
sudo dnf info nginx
sudo dnf install nginx
sudo systemctl enable --now nginx
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
sudo restorecon -Rv /var/www/html
```

Why: The commands target CentOS Stream or 8+, use `dnf`, manage the service through systemd, use `firewalld`, and preserve SELinux labeling.

**Bad:**

```bash
sudo yum install nginx
sudo iptables -F
sudo setenforce 0
```

Why: The commands do not identify the CentOS release, flush firewall rules destructively, and disable SELinux instead of adjusting policy.

## Conventions

| Rule | Rationale |
| --- | --- |
| Identify CentOS Stream versus legacy CentOS before giving commands | Package managers, repositories, and support status differ. |
| Use `dnf` for Stream and 8+, and `yum` for CentOS 7 | Commands match the platform's native tooling. |
| Verify repositories with GPG checks enabled | Package installation remains trustworthy. |
| Use `dnf info`, `yum info`, and `dnf repoquery` for package details | Operators can inspect package source and metadata. |
| Use `dnf versionlock` or `yum versionlock` for stability when needed | Critical package versions do not drift unexpectedly. |
| Call out EPEL dependencies explicitly | Extra repositories are deliberate and reversible. |
| Use `/etc/sysconfig/`, systemd drop-ins, and `systemctl` for services | Configuration follows RHEL-compatible conventions. |
| Prefer `firewalld` and `firewall-cmd` | Firewall guidance matches CentOS defaults. |
| Keep SELinux enforcing and use `semanage`, `restorecon`, and `setsebool` | Security remains active while policy is adjusted correctly. |
| Include validation and rollback for risky changes | Operators can confirm success and recover safely. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| State whether commands target CentOS Stream, CentOS 8+, or CentOS 7 | Give generic CentOS commands that may not work. |
| Use `dnf` on Stream and 8+ | Force `yum` examples onto newer systems without reason. |
| Enable EPEL only when needed and explain how to disable it | Treat EPEL as an unmentioned default dependency. |
| Use `firewall-cmd` for firewalld changes | Flush or bypass firewall rules without context. |
| Inspect `/var/log/audit/audit.log` for SELinux denials | Disable SELinux to make an error disappear. |
| Use `restorecon`, `semanage`, or `setsebool` for SELinux fixes | Edit labels or policies blindly. |
| Provide verification and rollback steps | Leave risky administration changes unvalidated. |

## Checklist Before Opening a PR

- [ ] The target CentOS version or Stream status is identified.
- [ ] Commands use `dnf` for Stream or 8+ and `yum` for CentOS 7.
- [ ] Repository guidance keeps GPG checks enabled.
- [ ] Package inspection uses `dnf info`, `yum info`, or `dnf repoquery` where relevant.
- [ ] Version pinning uses `dnf versionlock` or `yum versionlock` when stability requires it.
- [ ] EPEL dependencies are called out with safe enable and disable guidance.
- [ ] Service environment files use `/etc/sysconfig/` where appropriate.
- [ ] Service overrides use systemd drop-ins and `systemctl`.
- [ ] Firewall guidance prefers `firewalld` and `firewall-cmd` unless another stack is explicitly required.
- [ ] SELinux stays enforcing where possible and uses `semanage`, `restorecon`, `setsebool`, and `/var/log/audit/audit.log` for policy work.
- [ ] Risky changes include verification and rollback steps.
