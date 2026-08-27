---
name: namecheap
description: >-
  Manage Namecheap DNS through the bundled Python API utility, including domain listing, DNS host
  record view/add/update/remove operations, nameserver changes, email forwarding, glue records,
  public IP detection, API setup, and credential checks. Use when the user mentions Namecheap, DNS
  records, domains, A, AAAA, CNAME, MX, TXT, URL, URL301, FRAME, MXE, nameservers, or Namecheap
  API setup.
---

<!-- Generated from harness/github-copilot/skills/namecheap/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Namecheap DNS management

Manage Namecheap domains and DNS records through the bundled `namecheap.py` utility while protecting API credentials and avoiding destructive record replacement. This is a UTILITY SKILL for add/change/remove DNS work, not registration/purchase.

## When to invoke

- "Add a DNS record in Namecheap."
- "Update this A record or CNAME."
- "List my Namecheap domains."
- "Show DNS records for this domain."
- "Configure the Namecheap API and whitelist my public IP."

## Prerequisites and context

- Use `namecheap.py` in this skill directory for all API interactions.
- The script requires Python 3 standard library only; no `pip install` is needed.
- Credentials come from `~/.namecheap-api` or environment variables.
- Namecheap API access must be enabled and the caller's public IP must be whitelisted at https://ap.www.namecheap.com/settings/tools/apiaccess/.

## Credential setup

Before any API operation, verify `~/.namecheap-api` exists and is readable or that `NAMECHEAP_API_USER` and `NAMECHEAP_API_KEY` are exported. If not configured:

1. Run `python3 namecheap.py public-ip` to display the public IP.
2. Instruct the user to enable API access at https://ap.www.namecheap.com/settings/tools/apiaccess/, select ON, and whitelist the displayed IP.
3. Have the user run `python3 namecheap.py setup` in their own terminal. The `setup` script prompts for username, reads the API key with `getpass`, writes `~/.namecheap-api`, applies `chmod 600` owner read/write permissions, and validates the connection.
4. Never ask the user to paste the API key into chat. Never log, echo, or display the key. If interactive setup is unavailable, instruct the user to export `NAMECHEAP_API_USER` and `NAMECHEAP_API_KEY` in their own shell.

Credential file format:

```bash
NAMECHEAP_API_USER="username"
NAMECHEAP_API_KEY="api-key-here"
```

Environment variables take precedence over the file.

## DNS operations

Show current records before modifying. Use `dns.addHost` and `dns.removeHost` for safe single-record changes because they perform fetch-modify-write internally. Confirm destructive changes with `ask_user`-style confirmation before removing records or replacing all records with `domains.dns.setHosts` / `setHosts`.

```bash
# Show public IP (for setup)
python3 namecheap.py public-ip

# Run setup flow
python3 namecheap.py setup

# List domains
python3 namecheap.py domains.getList

# Get nameservers for a domain (shows if using Namecheap DNS or custom)
python3 namecheap.py domains.dns.getList --domain example.com

# Get DNS records for a domain
python3 namecheap.py domains.dns.getHosts --domain example.com

# Add a single record (preserves existing records)
python3 namecheap.py dns.addHost --domain example.com --type A --name www --address 1.2.3.4 --ttl 1800

# Remove a single record
python3 namecheap.py dns.removeHost --domain example.com --type A --name www --address 1.2.3.4

# Replace all records from a JSON file
python3 namecheap.py domains.dns.setHosts --domain example.com --hosts records.json

# Switch to Namecheap default DNS
python3 namecheap.py domains.dns.setDefault --domain example.com

# Switch to custom nameservers
python3 namecheap.py domains.dns.setCustom --domain example.com --nameservers ns1.cloudflare.com,ns2.cloudflare.com

# Get email forwarding rules
python3 namecheap.py domains.dns.getEmailForwarding --domain example.com

# Set email forwarding (single rule)
python3 namecheap.py domains.dns.setEmailForwarding --domain example.com --mailbox info --forward-to user@gmail.com

# Set email forwarding (from JSON file)
python3 namecheap.py domains.dns.setEmailForwarding --domain example.com --forwards forwards.json

# Create a child nameserver (glue record)
python3 namecheap.py domains.ns.create --domain example.com --nameserver ns1.example.com --ip 1.2.3.4

# Delete a child nameserver
python3 namecheap.py domains.ns.delete --domain example.com --nameserver ns1.example.com

# Get nameserver info
python3 namecheap.py domains.ns.getInfo --domain example.com --nameserver ns1.example.com

# Update nameserver IP
python3 namecheap.py domains.ns.update --domain example.com --nameserver ns1.example.com --old-ip 1.2.3.4 --ip 5.6.7.8
```

Supported record types: A, AAAA, CNAME, MX, MXE, TXT, URL, URL301, FRAME.

## JSON file formats

`domains.dns.setHosts --hosts records.json` expects an array of Namecheap API field names:

```json
[
  { "HostName": "@", "RecordType": "A", "Address": "1.2.3.4", "TTL": 1800 },
  { "HostName": "www", "RecordType": "CNAME", "Address": "@", "TTL": 1800 },
  { "HostName": "@", "RecordType": "MX", "Address": "mail.example.com.", "TTL": 1800, "MXPref": 10 }
]
```

`domains.dns.setEmailForwarding --forwards forwards.json` expects mailbox rules:

```json
[
  { "MailBox": "info", "ForwardTo": "team@example.net" },
  { "MailBox": "sales", "ForwardTo": "owner@example.net" }
]
```

## Gotchas

- **`domains.dns.setHosts` replaces ALL records**: never call it until you have fetched all existing records and confirmed the replacement.
- **Explain TTL in human terms**: 1800 = 30 minutes and 3600 = 1 hour.
- **Handle multi-part TLDs**: domains such as `example.co.uk` have SLD=`example` and TLD=`co.uk`. The script has a built-in, best-effort second-level suffix list including `co.uk`, `com.au`, `co.jp`, and `com.br`, not a full public-suffix database. Error `2019166` ("Domain not found") can mean the SLD/TLD split was wrong; confirm the registered domain with the user.
- **Out of scope**: do not use this skill for domain registration/purchase, SSL certificate management, hosting configuration, or non-Namecheap DNS providers.

## Progressive disclosure and bundled resources

- `namecheap.py`: standard-library Python utility for Namecheap API operations.
- `references/namecheap-api.md`: request/response details for Namecheap API commands.

## Output template

```markdown
## Namecheap DNS result — <domain>

**Status:** changed | reviewed | blocked
**Operation:** <public-ip | setup | list domains | get hosts | add host | remove host | set hosts | nameserver | email forwarding>

| Step | Command | Result |
| --- | --- | --- |
| Credential check | `<command or file check>` | <configured or setup needed> |
| Current records | `python3 namecheap.py domains.dns.getHosts --domain <domain>` | <summary> |
| Change | `<namecheap.py command>` | <success, skipped, or blocked> |

**TTL explanation:** <human-readable TTL if relevant>
**Confirmation required:** yes | no | already provided
```

## Quality gate

- [ ] Credentials were checked before API operations.
- [ ] API keys were never requested, displayed, logged, or placed in chat.
- [ ] Current DNS records were fetched before add, remove, or replacement operations.
- [ ] Destructive removal or `domains.dns.setHosts` replacement was confirmed.
- [ ] Single-record changes used `dns.addHost` or `dns.removeHost` where possible.
- [ ] Multi-part TLD and `2019166` cases were handled explicitly.
- [ ] TTL values were explained in human terms when relevant.

## References

- [Namecheap API access settings](https://ap.www.namecheap.com/settings/tools/apiaccess/)
