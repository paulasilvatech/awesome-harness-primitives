---
applyTo: "**"
description: "Enforces Arch Linux administration conventions for pacman upgrades, AUR caution, systemd configuration, troubleshooting, security, validation, and rollback guidance."
---

# Arch Linux Conventions — Rolling-Release Administration

These instructions apply when writing guidance, scripts, or documentation for Arch Linux systems. They are authoritative for Arch-specific package management, rolling-release safety, configuration placement, service handling, security posture, and validation commands; user-provided machine facts and the Arch Wiki win where they provide more current system-specific guidance.

## Platform Alignment

Arch is a rolling-release distribution, so treat system state as time-sensitive. Confirm the current kernel, release-relevant package versions, and recent package changes before diagnosing failures that could be caused by partial upgrades, ABI drift, or out-of-date services.

| Concern | Convention |
| --- | --- |
| Upgrade model | Emphasize full upgrades with `pacman -Syu`; avoid partial upgrades. |
| Authority | Prefer official repositories and the Arch Wiki for decisions that depend on current Arch policy. |
| Troubleshooting context | Collect `uname -r`, package versions, and recent transaction history before recommending invasive fixes. |
| Reboot awareness | Note reboot requirements after kernel, glibc, systemd, graphics stack, or other core library upgrades. |

## Package Management

Use `pacman` directly for official repositories. Make commands copy-paste-ready and explain whether they inspect, install, upgrade, remove, or clean packages.

| Task | Command pattern |
| --- | --- |
| Full system upgrade | `sudo pacman -Syu` |
| Package metadata | `pacman -Qi <package>` |
| Package file list | `pacman -Ql <package>` |
| Repository search | `pacman -Ss <term>` |
| Installed package search | `pacman -Qs <term>` |
| Owning package for a file | `pacman -Qo <path>` |
| Transaction log | `grep pacman /var/log/pacman.log` or inspect `/var/log/pacman.log` directly. |

Mention AUR helpers only with explicit cautions: review the `PKGBUILD`, understand the maintainer and source URLs, and prefer official packages when available. Do not present AUR helper output as equivalent to official repository trust.

## Configuration, Services, and Logs

Keep administrator-owned configuration under `/etc`. Avoid editing files under `/usr` because package upgrades can overwrite them and because `/usr` should represent vendor-managed content.

Use systemd drop-ins for service overrides: `/etc/systemd/system/<unit>.d/override.conf`. Run `sudo systemctl daemon-reload` after changing unit files or drop-ins, then use `systemctl status <unit>` and `journalctl -u <unit>` to verify behavior.

## Security and Network Controls

Recommend least-privilege `sudo` usage, minimal packages, and explicit firewall choices. Call out whether the system uses `nftables/ufw`, nftables directly, or a frontend such as `ufw`; do not assume a firewall is active without checking.

Treat secrets in shell history, world-readable files, and pasted logs as sensitive. Redact tokens, private keys, passwords, and host-specific secrets from commands and examples.

## Deliverables and Validation

Provide concrete commands in fenced `bash` blocks, then include validation and rollback or cleanup steps for risky operations. Prefer reversible changes: package install/remove commands, systemd override removal, service restart validation, and log checks.

## Good / Bad Examples

The examples below illustrate safe package guidance for a rolling-release system.

**Good:**

```bash
sudo pacman -Syu
pacman -Qi openssl
systemctl status sshd
journalctl -u sshd --since "1 hour ago"
```

Why: The sequence upgrades fully, inspects package state, and validates the affected service before deeper changes.

**Bad:**

```bash
sudo pacman -Sy openssl
sudo sed -i 's/example/bad/' /usr/lib/systemd/system/sshd.service
```

Why: `pacman -Sy` risks a partial upgrade, and editing `/usr` package files creates changes that upgrades can overwrite.

## Conventions

| Rule | Rationale |
|---|---|
| Use `pacman -Syu` for upgrades and avoid partial upgrades | Rolling-release dependencies expect the whole system to move together. |
| Inspect packages with `pacman -Qi`, `pacman -Ql`, `pacman -Ss`, `pacman -Qs`, and `pacman -Qo` before changing them | Package facts reduce guesswork and prevent removing the wrong dependency. |
| Treat the Arch Wiki and official repositories as the default authority | Arch-specific guidance changes quickly and community copies can lag. |
| Keep configuration in `/etc` and use systemd drop-ins under `/etc/systemd/system/<unit>.d/` | Administrator changes survive package upgrades and remain auditable. |
| Use `systemctl` and `journalctl` for service control and logs | systemd is the service manager and log source on standard Arch systems. |
| Include validation plus rollback or cleanup commands for risky operations | Users need a safe exit path when a package, service, or firewall change fails. |

## Do / Do Not

| Do | Do not |
|---|---|
| Recommend `sudo pacman -Syu` before package troubleshooting | Recommend `pacman -Sy <package>` as a routine fix. |
| Review AUR `PKGBUILD` files before building | Treat AUR helpers as trusted package managers. |
| Create systemd overrides in `/etc/systemd/system/<unit>.d/` | Edit packaged unit files in `/usr`. |
| Check `journalctl -u <unit>` after service changes | Declare a service fixed without checking logs. |
| State nftables or `ufw` assumptions explicitly | Assume firewall behavior without inspection. |

## Checklist Before Opening a PR

- [ ] Guidance reflects Arch as a rolling-release system and avoids partial upgrades.
- [ ] Package commands use `pacman` inspection or full-upgrade patterns correctly.
- [ ] AUR advice includes `PKGBUILD` review and support caveats.
- [ ] Configuration changes belong under `/etc`, with systemd drop-ins when units are customized.
- [ ] Service guidance includes `systemctl` and `journalctl` validation.
- [ ] Security guidance covers least privilege, minimal packages, reboot needs, and explicit firewall tooling.
- [ ] Risky changes include rollback or cleanup commands.
