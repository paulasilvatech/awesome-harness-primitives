---
applyTo: "**/*.yaml,**/*.yml"
description: "Enforces Ansible conventions for playbook naming, inventory, idempotency, privilege, secret management, YAML style, and validation. Use when editing Ansible YAML files."
---

# Ansible Conventions — Idempotent YAML Automation

These instructions apply to YAML files that define Ansible playbooks, roles, variables, inventory, and task includes. They are authoritative for Ansible naming, idempotency, FQCN usage, privilege boundaries, secret management, style, and validation in matched files; repository-specific role layout, inventory policy, and security requirements win where they define stricter rules.

## General Playbook Conventions

- Use Ansible to configure and manage infrastructure, and keep configurations in version control.
- Keep things simple; use advanced features only when necessary.
- Give every play, block, and task a concise but descriptive `name`.
- Start names with an action verb such as `Install`, `Configure`, or `Copy`.
- Capitalize the first letter of task names and omit periods at the end.
- Omit the role name from role tasks because Ansible displays the role name automatically.
- When including tasks from a separate file, include the filename in task names only when it helps locate them, using `<TASK_FILENAME> : <TASK_NAME>`.
- Use comments for additional context about what, how, and/or why something is done; do not include redundant comments.
- Group related tasks together for readability and modularity.

## Inventory, Idempotency, and Privilege

| Concern | Convention |
| --- | --- |
| Dynamic inventory | Use dynamic inventory for cloud resources and tags to create groups by environment, function, location, or similar attributes. |
| Variables | Use `group_vars` to set variables based on dynamic inventory attributes. |
| Idempotency | Use idempotent Ansible modules whenever possible. |
| Shell escape hatch | Avoid `shell`, `command`, and `raw`; when unavoidable, use `creates:` or `removes:` where feasible. |
| FQCN | Use fully qualified collection names (FQCN) so the correct module or plugin is selected. |
| Builtins | Use the `ansible.builtin` collection for builtin modules and plugins. |
| State | Explicitly set `state: present` or `state: absent` when a module's state is optional. |
| Privilege | Use the lowest privileges necessary; set `become: true` at play, `host`, or `include:` scope only when all included tasks require super user privileges, otherwise set it at task scope. |

## Secret Management

When using Ansible alone, store secrets with Ansible Vault and keep vaulted variable origins easy to find.

| File or variable | Convention |
| --- | --- |
| `group_vars/` | Create a subdirectory named after the group. |
| `vars` | Define all variables needed by playbooks, including sensitive variables that reference vaulted values. |
| `vault` | Copy sensitive variables into this file and prefix names with `vault_`. |
| Jinja reference | In `vars`, point to vaulted values with syntax such as `db_password: "{{ vault_db_password }}"`. |
| Encryption | Encrypt the `vault` file before committing or distributing it. |
| Playbook usage | Use the variable name from `vars`, not the `vault_` name, in playbooks. |

When using other tools with Ansible, such as Terraform, store secrets in a third-party secrets management tool such as Hashicorp Vault or AWS Secrets Manager so every tool references a single source of truth.

## YAML Style and Ordering

- Use 2-space indentation and always indent lists.
- Separate two host blocks, two task blocks, and host/include blocks with a single blank line.
- Use `snake_case` for variable names.
- Sort variables alphabetically in `vars:` maps and variable files.
- Always use multi-line map syntax, regardless of how many pairs the map contains.
- Prefer single quotes over double quotes.
- Use double quotes only when nested inside single quotes or when escaping characters such as `"\n"`.
- Use folded block scalar syntax `>` for long strings where newlines become spaces and literal block scalar syntax `|` when preserving newlines.

Order play sections as `hosts`, host options alphabetically such as `become`, `remote_user`, and `vars`, then `pre_tasks`, `roles`, and `tasks`. Order tasks as `name`, task declaration such as `service:` or `package:`, task parameters in multi-line map syntax, loop operators such as `loop`, task options alphabetically such as `become`, `ignore_errors`, and `register`, then `tags`. Quote filenames in `include` statements and only insert blank lines between multi-line includes.

## Linting and Dry Runs

Use `ansible-lint` and `yamllint` to enforce syntax and style. Use `ansible-playbook --syntax-check` for syntax validation and `ansible-playbook --check --diff` for dry-run execution before risky changes.

## Good / Bad Examples

The examples below illustrate FQCN usage, naming, idempotency, and state.

**Good**

```yaml
- name: Configure web package
  ansible.builtin.package:
    name: nginx
    state: present
  become: true
```

Why: the task has an action-oriented name, uses `ansible.builtin`, declares `state: present`, and scopes privilege to the task.

**Bad**

```yaml
- name: nginx.
  shell: apt install nginx -y
  become: true
```

Why: the task name is weak, the `shell` command is not idempotent, and the module is not fully qualified.

## Conventions

| Rule | Rationale |
| --- | --- |
| Name every play, block, and task with a concise action verb and no trailing period. | Runs and failures are easy to scan. |
| Prefer idempotent modules, FQCN, explicit `state`, and `ansible.builtin` for builtins. | Repeated playbook runs converge safely and select the intended plugin. |
| Use dynamic inventory, tags, and `group_vars` for cloud resources. | Inventory reflects changing infrastructure without hardcoded host lists. |
| Keep secrets in Ansible Vault or a shared external secrets manager when multiple tools participate. | Sensitive values stay encrypted and do not drift between tools. |
| Use 2-space YAML, `snake_case`, sorted variables, multi-line maps, and consistent quoting. | Reviews stay small and style remains predictable. |
| Validate with `ansible-lint`, `yamllint`, `ansible-playbook --syntax-check`, and `ansible-playbook --check --diff`. | Syntax, style, and idempotent behavior are checked before execution. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `creates:` or `removes:` when `shell` or `command` is unavoidable. | Use `shell`, `command`, or `raw` for work an Ansible module can do. |
| Set `become: true` only where elevated privileges are required. | Set play-level `become: true` when only one task needs privilege. |
| Use `db_password: "{{ vault_db_password }}"` in `vars`. | Reference `vault_` variables directly throughout playbooks. |
| Use folded `>` or literal `|` block scalars for long strings. | Cram long escaped strings into one quoted line. |
| Quote include filenames. | Add blank lines between simple one-line include statements. |

## Checklist Before Opening a PR

- [ ] Plays, blocks, and tasks have concise action-oriented `name` values without trailing periods.
- [ ] Modules use FQCN and builtins use `ansible.builtin`.
- [ ] Tasks are idempotent, avoid `shell`, `command`, and `raw`, or use `creates:`/`removes:` when those commands are necessary.
- [ ] Optional states are explicit as `state: present` or `state: absent`.
- [ ] Privilege escalation is scoped to the smallest play, include, or task that needs it.
- [ ] Secrets use Ansible Vault with `group_vars/`, `vars`, `vault`, `vault_` prefixes, or a shared external secrets manager.
- [ ] YAML uses 2-space indentation, indented lists, `snake_case`, sorted variables, multi-line maps, and the required quoting style.
- [ ] `ansible-lint`, `yamllint`, `ansible-playbook --syntax-check`, and relevant `ansible-playbook --check --diff` validations pass.

## References

- Fully qualified collection names (FQCN): https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html#term-Fully-Qualified-Collection-Name-FQCN
- Builtin modules and plugins: https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html#plugin-index
- Ansible Documentation - Tips and Tricks: https://docs.ansible.com/ansible/latest/tips_tricks/index.html
- Whitecloud Ansible Styleguide: https://github.com/whitecloud/ansible-styleguide
