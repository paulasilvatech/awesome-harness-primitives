<!-- Generated from harness/github-copilot/instructions/fedora-linux.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Fedora administration conventions for dnf package workflows, systemd, firewalld, SELinux, validation, compatibility, and rollback guidance.

# Fedora Conventions — Red Hat Family Administration

These instructions apply when writing guidance, scripts, or documentation for Fedora systems. They are authoritative for Fedora package management, systemd service handling, firewalld use, SELinux-safe remediation, compatibility notes, verification, and rollback; user-provided host facts and current Fedora documentation win where they provide release-specific constraints.

## Platform Alignment

State the Fedora release number when it affects commands, package names, repositories, or compatibility. Fedora moves quickly, so confirm older guidance before applying it to a current release and note when a command applies broadly across the Red Hat family versus Fedora specifically.

Prefer modern tooling: `dnf` for package operations, `systemctl` for services, `journalctl` for logs, and `firewall-cmd` for firewalld. Use `rpm` for low-level package inspection when it gives facts that `dnf` does not surface directly.

## Package Management

| Task | Command pattern |
| --- | --- |
| Install packages | `sudo dnf install <package>` |
| Update packages | `sudo dnf upgrade` |
| Inspect repository metadata | `dnf info <package>` |
| Inspect installed package | `rpm -qi <package>` |
| List package files | `rpm -ql <package>` |
| Review transactions | `dnf history` |
| Roll back a transaction | `sudo dnf history undo <transaction-id>` |

Mention COPR repositories only with clear support caveats. Treat COPR packages as third-party builds that may not receive the same support, testing, or lifecycle guarantees as Fedora repositories.

## Configuration, Services, and Logs

Use systemd drop-ins in `/etc/systemd/system/<unit>.d/` for service overrides. After changing unit files or drop-ins, run `sudo systemctl daemon-reload`, restart or reload the affected service, and verify with `systemctl status <unit>` plus `journalctl -u <unit>`; write `systemctl status` examples with the unit name filled in.

Prefer `firewalld` and `firewall-cmd` unless the task explicitly uses `nftables`. Make zone, service, port, and permanence explicit so firewall changes are understandable and repeatable.

## SELinux and Security

Keep SELinux enforcing unless the user explicitly requests permissive mode for diagnosis. Prefer targeted fixes with `semanage`, `setsebool`, and `restorecon` instead of broad policy generation.

| Need | Preferred command family |
| --- | --- |
| Restore file labels | `restorecon -Rv <path>` |
| Manage booleans | `setsebool -P <boolean> on|off` |
| Add file context rules | `semanage fcontext -a -t <type> '<path-regex>'` |
| Inspect denials | `ausearch -m avc` or `journalctl` with SELinux context. |

Use `audit2allow` cautiously and only after explaining why a narrower label, boolean, or service configuration fix is insufficient.

## Deliverables and Rollback

Provide copy-paste-ready command blocks, verification steps after changes, and rollback steps for risky operations. Rollback may use `dnf history undo`, removal of a systemd drop-in, firewall rule deletion, or SELinux context restoration.

## Good / Bad Examples

The examples below illustrate a targeted SELinux and service fix.

**Good:**

```bash
sudo semanage fcontext -a -t httpd_sys_content_t '/srv/site(/.*)?'
sudo restorecon -Rv /srv/site
sudo systemctl restart httpd
systemctl status httpd
```

Why: The fix labels the intended path, restores contexts, restarts the affected service, and verifies health.

**Bad:**

```bash
sudo setenforce 0
audit2allow -a -M local && sudo semodule -i local.pp
```

Why: It disables enforcement and creates broad policy before trying targeted Fedora SELinux tools.

## Conventions

| Rule | Rationale |
|---|---|
| State the Fedora release when compatibility matters | Fedora's fast cadence can make old package and service advice wrong. |
| Use `dnf`, `rpm -qi`, and `dnf history` for package facts and rollback | Package changes become inspectable and reversible. |
| Use systemd drop-ins under `/etc/systemd/system/<unit>.d/` | Overrides survive package updates and remain separate from vendor units. |
| Prefer `firewalld` and `firewall-cmd` unless `nftables` is explicitly chosen | Fedora defaults are easier to audit and support. |
| Keep SELinux enforcing and use `semanage`, `setsebool`, and `restorecon` for targeted fixes | Security remains active while resolving policy mismatches. |
| Include verification and rollback commands for risky changes | Administrators can prove the change worked and undo it safely. |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `sudo dnf upgrade` and `dnf info` for package workflows | Mix Fedora guidance with unsupported package-manager commands. |
| Use `dnf history` before and after risky package changes | Leave users without a rollback path. |
| Manage services with `systemctl` and logs with `journalctl` | Diagnose services without checking the systemd status or logs. |
| Use `firewall-cmd --permanent` plus reload when persistence is intended | Add transient firewall rules while implying they persist. |
| Fix SELinux with labels, booleans, and context restoration first | Disable SELinux or generate broad `audit2allow` policy as the first response. |

## Checklist Before Opening a PR

- [ ] Guidance states the Fedora release when release-specific behavior matters.
- [ ] Package workflows use `dnf`, `rpm -qi`, and `dnf history` appropriately.
- [ ] COPR advice includes support and trust caveats.
- [ ] Service changes use systemd drop-ins and include daemon reload, restart or reload, status, and log validation.
- [ ] Firewall guidance uses `firewall-cmd` or explicitly justifies `nftables`.
- [ ] SELinux remains enforcing unless permissive mode is explicitly requested for diagnosis.
- [ ] Risky operations include verification and rollback steps.
