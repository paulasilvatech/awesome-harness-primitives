---
applyTo: "**/*.{md,js,mjs,cjs,ts,tsx,jsx,py,json}"
description: "Enforces generic cliche placeholder data in documentation, examples, templates, comments, and sample configuration instead of real or sensitive implementation data."
---

# Cliche Documentation Data Conventions — Placeholder Safety

These instructions apply to documentation, examples, sample scripts, templates, README content, CHANGELOG entries, and committed comments in matched Markdown, JavaScript, TypeScript, Python, and JSON files. They are authoritative for replacing real implementation data with generic cliche placeholders; product requirements, runtime code, or local configuration may contain real values only when those values are required for execution and are not copied into documentation.

## Public Documentation Boundary

Never include real data from prompts, local files, scripts, configuration, task files, map or filter files, git-ignored files, or implementation-specific sources in documentation. Documentation examples use only well-known, fictional, or obviously placeholder values. A stranger should be able to read every example and learn nothing about the real users, clients, organizations, accounts, domains, or operations behind the tool.

Real data may exist in runtime code, local scripts, local configuration, git-ignored files, and prompt context when needed to build or configure a tool. It does not belong in README.md, docs folders, example templates, CHANGELOG.md entries, or committed code comments.

## Data That Must Be Replaced

Replace values originating from `config.json`, `.env`, account modules, batch scripts, shell scripts, task runners, user prompts, JSON mappings, extraction rules, git-ignored files, and environment-specific configuration. Treat real names, email addresses, organization details, domain names, client identifiers, account names, credentials, and organization-specific terminology as documentation leaks.

A word from real data may appear only when it is a common English word used in its ordinary sense and not as an example value.

## Approved Placeholder Data

| Category | Approved examples |
| --- | --- |
| People | Jane Doe, John Smith, Alice, Bob |
| Email addresses | `jane.doe@example.com`, `admin@example.org` |
| Organizations | Acme Corp, Contoso, Northwind Traders |
| Domains | `example.com`, `example.org`, `example.net` |
| Addresses | 123 Main Street, Suite 100, Springfield |
| Phone numbers | `(555) 123-4567` |
| Accounts and usernames | `demo-user`, `test-account` |
| File paths | `accounts/acme.mjs`, `config/reports.json` |
| Project names | My Project, Sample App, Demo Tool |

## Context-Matched Placeholders

| OS or context | Use | Avoid |
| --- | --- | --- |
| Windows per-user data | `C:\Users\<user>\AppData\Local\AcmeApp\` | `/home/user/...`, `~/.config/...` |
| Windows machine-wide data | `C:\ProgramData\AcmeApp\` | `C:\Users\<user>\...` |
| Windows temporary | `%TEMP%\acme\` or `C:\Users\<user>\AppData\Local\Temp\acme\` | `/tmp/acme/` |
| POSIX per-user data | `~/.config/acme/`, `~/.local/share/acme/` | `C:\Users\<user>\...` |
| POSIX temporary | `/tmp/acme/` | `%TEMP%\acme\` |
| Cross-platform examples | `<config-dir>/acme/` or show both forms | One platform silently |

| Data role | Plausible location |
| --- | --- |
| Per-user logs and runtime output | `C:\Users\<user>\AppData\Local\<App>\logs\`, `~/.local/state/<app>/` |
| Per-user settings | `%APPDATA%\<App>\`, `~/.config/<app>/` |
| Machine-wide shared state | `C:\ProgramData\<App>\`, `/var/lib/<app>/` |
| Project-local working files | `./build/`, `./tmp/` |
| Generated output artifacts | `./dist/`, `./out/` |

Match identifiers to the domain: use `acme-corp` or `northwind-traders` for CRM, `springfield` or `region-west` for geographic data, and `demo-app` or `sample-project` for developer tooling.

## Documentation Examples

When documenting a feature built with real account data, replace the real account with a fictional one.

```javascript
// accounts/acme.mjs — Example account configuration
export default {
  name: 'Acme Corp',
  email: 'reports@example.com',
  folder: 'INBOX',
};
```

When documenting configuration, replace real domains, paths, and credentials.

```json
{
  "host": "imap.example.com",
  "user": "admin@example.com",
  "folder": "INBOX/Reports",
  "outputDir": "./downloads"
}
```

When documenting scripts, use generic organizations and parameters.

```batch
@echo off
REM Example: Run the extraction task for Acme Corp
node extractEmail.mjs --account acme --task download
```

## Technical Vocabulary

Preserve these source terms when they apply to edits in this domain: `.bat` `.jsx` `<install-dir>` `C:\ProgramData\…` `bash` `geographic-data` `install-dir` `machine-shared` `per-machine` `public-facing` `user-driven` `~/.config/…`.

## Good / Bad Examples

The examples below show replacing implementation-specific values with cliche data.

**Good:**

```md
Configure the sample account `acme` with `admin@example.org` and write output to `./dist/`.
```

Why: The account, email, and path are generic and plausible for documentation.

**Bad:**

```md
Copy the customer domain and account ID from the local `.env` file into the README example.
```

Why: It instructs authors to leak local implementation data into public docs.

## Conventions

| Rule | Rationale |
|---|---|
| Replace prompt, script, config, task, and git-ignored data before documenting | Local implementation data can expose private organizations or accounts |
| Use only approved cliche placeholders in public examples | Familiar placeholders communicate shape without leaking reality |
| Match placeholder syntax to the OS shown in the example | Incorrect paths mislead readers and make examples unusable |
| Match placeholder location to data role | User, machine, runtime, config, and generated data belong in different places |
| Match identifiers to the example domain | Generic data still needs to be plausible in context |
| Keep CHANGELOG and committed comments generic | Public history and source comments are documentation too |

## Do / Do Not

| Do | Do not |
|---|---|
| Use Jane Doe, Acme Corp, Contoso, and `example.com` | Use real people, customers, organizations, or domains |
| Use `accounts/acme.mjs` and `config/reports.json` in docs | Copy local account module names when they identify real entities |
| Use platform-correct placeholders such as `%TEMP%\acme\` in Windows examples | Mix POSIX paths into Windows-only snippets |
| Use `<config-dir>` for platform-neutral examples | Pretend one OS path fits all platforms |
| Describe changes generically in CHANGELOG.md | Include private account names in release notes |
| Keep real values only in runtime code when required | Move runtime secrets, contacts, or domains into README examples |

## Checklist Before Opening a PR

- [ ] Documentation examples contain only approved cliche or clearly abstract placeholder values.
- [ ] No value from prompts, local config, scripts, task files, maps, filters, or git-ignored files appears in docs.
- [ ] Paths match the operating system and data role shown in the example.
- [ ] Identifiers match the surrounding domain vocabulary without revealing real entities.
- [ ] README.md, docs content, CHANGELOG.md, templates, and committed comments are free of real data.
- [ ] Runtime code and documentation remain separated when real values are required for execution.
