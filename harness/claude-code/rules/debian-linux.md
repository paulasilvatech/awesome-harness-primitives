<!-- Generated from harness/github-copilot/instructions/debian-linux.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Debian-based Linux administration conventions for apt workflows, package sources, configuration files, services, security, validation, and rollback guidance.

# Debian Linux Administration Conventions — Apt and Policy-Aligned Operations

These instructions apply when writing guidance, scripts, or documentation for Debian-based Linux systems. They are authoritative for Debian release alignment, apt workflows, package inspection, configuration paths, systemd services, firewall guidance, AppArmor awareness, validation, and rollback expectations; task-specific operational runbooks and environment policy win where they impose stricter production controls.

## Platform Alignment

Favor Debian Stable defaults and long-term support expectations. Call out the Debian release, such as `bookworm` or `bullseye`, when commands or package availability depend on it. Prefer official Debian repositories before recommending third-party sources, and explain any repository addition or apt pinning.

## Package Management

Use the right apt-family tool for the audience and context, and provide copy-paste-ready commands when giving deliverables.

| Task | Convention |
| --- | --- |
| Interactive package operations | Use `apt` for commands a human runs directly. |
| Scripts and automation | Use `apt-get` because its interface is more stable for scripts. |
| Package source inspection | Use `apt-cache policy`, `apt show`, and `dpkg -l`. |
| Manual versus automatic packages | Use `apt-mark` to track manual, automatic, and auto-installed package intent. |
| Apt pinning | Document entries in `/etc/apt/preferences.d/` and explain the reason. |

Keep package installs minimal and avoid adding third-party repositories unless official Debian packages cannot satisfy the requirement.

## Configuration, Services, and Firewall

Store configuration under `/etc` and avoid modifying files under `/usr` directly. Use systemd drop-ins in `/etc/systemd/system/<unit>.d/` for service overrides. Use `systemctl` for service control and `journalctl` for logs. Use `ufw` or `nftables` for firewall guidance, and state which firewall stack is expected before giving commands.

## Security, Verification, and Rollback

Account for AppArmor profiles when services need filesystem, network, or capability changes. Recommend least-privilege `sudo` usage and minimal package installs. Include verification commands after security changes and rollback steps for destructive or risky operations.

## Good / Bad Examples

The examples below illustrate script-safe package installation and service validation.

**Good:**

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends nginx
systemctl status nginx --no-pager
journalctl -u nginx --no-pager -n 50
```

Why: The commands use `apt-get` for scriptable installation, avoid extra packages, and verify service state and logs without a pager.

**Bad:**

```bash
sudo apt install nginx -y
sudo sed -i 's/default/custom/' /usr/lib/systemd/system/nginx.service
```

Why: The command mixes interactive `apt` into automation and edits vendor-owned `/usr` files instead of using `/etc` configuration or a systemd drop-in.

## Conventions

| Rule | Rationale |
| --- | --- |
| Name the Debian release when behavior depends on it | Package names and defaults differ between releases. |
| Prefer official Debian repositories | Official packages reduce supply-chain and maintenance risk. |
| Use `apt` interactively and `apt-get` in scripts | Commands match the stability expectations of each interface. |
| Inspect packages with `apt-cache policy`, `apt show`, and `dpkg -l` | Operators can verify versions and origins before changing systems. |
| Put configuration in `/etc` and service overrides in `/etc/systemd/system/<unit>.d/` | Local changes survive package upgrades and avoid vendor file edits. |
| Use `systemctl` and `journalctl` for service operations | Service state and logs are collected through the system manager. |
| Account for AppArmor, least privilege, and minimal installs | Security posture remains tight while changes are made. |
| Include validation and rollback for risky changes | Operators can prove success and recover safely. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Say whether guidance targets `bookworm`, `bullseye`, or another release | Assume all Debian releases have identical packages. |
| Use `apt-get` in scripts | Use interactive-only apt behavior in automation. |
| Document apt pins in `/etc/apt/preferences.d/` | Add unexplained pinning that changes package resolution. |
| Override services with systemd drop-ins | Edit unit files under `/usr` directly. |
| State whether `ufw` or `nftables` is expected | Mix firewall tools without explanation. |
| Verify security changes with commands | Leave operators without proof that the change worked. |
| Provide rollback for destructive actions | Make one-way system changes without recovery guidance. |

## Checklist Before Opening a PR

- [ ] Debian release assumptions are stated when relevant.
- [ ] Official Debian repositories are preferred, and any third-party source is justified.
- [ ] Interactive examples use `apt`; scripts use `apt-get`.
- [ ] Package inspection uses `apt-cache policy`, `apt show`, or `dpkg -l` where needed.
- [ ] Manual package state uses `apt-mark` when relevant.
- [ ] Apt pinning is documented in `/etc/apt/preferences.d/` with a reason.
- [ ] Configuration changes are under `/etc`, not direct edits under `/usr`.
- [ ] Service changes use `/etc/systemd/system/<unit>.d/`, `systemctl`, and `journalctl`.
- [ ] Firewall guidance names `ufw` or `nftables`.
- [ ] AppArmor, least privilege, validation commands, and rollback steps are covered for risky changes.
