---
name: sandbox-npm-install
description: >-
  Install npm packages in a Docker sandbox with virtiofs-mounted workspaces by installing node_modules on local ext4 storage and symlinking back. Use when installing, reinstalling, or updating packages, or when native binaries such as esbuild, lightningcss, rollup, or vite crash with mmap, SIGILL, or SIGSEGV errors.
---

# Sandbox npm install

Install Node.js dependencies safely in Docker sandbox environments where the workspace is mounted through virtiofs by running npm on container-local ext4 storage, symlinking `node_modules` back, and verifying native binaries.

## When to invoke

- "Install npm packages in this sandbox."
- "Reinstall node_modules after package.json changed."
- "Fix esbuild or rollup crashing on virtiofs."
- "Native binaries fail with SIGILL, SIGSEGV, mmap, or unaligned sysNoHugePageOS."
- "Install Playwright Chromium in the sandbox."

## Prerequisites and context

- A Docker sandbox environment with a virtiofs-mounted workspace.
- Node.js and npm available in the container.
- A `package.json` file in the target workspace.
- Use the bundled script from this skill package; do not run `npm ci` or `npm install` directly in the mounted workspace.

## Why the script is required

Docker sandbox workspaces are typically mounted via virtiofs for host-to-Linux-VM file sync. Native Go and Rust binaries such as `esbuild`, `lightningcss`, `rollup`, and `vite` can crash with mmap alignment failures on aarch64 when executed from virtiofs. Installing dependencies on the container's local ext4 filesystem and symlinking `node_modules` back avoids those crashes.

The local install directory, for example `/home/agent/project-deps`, is container-local and is not synced to the host. The `node_modules` symlink may look broken on the host; that is harmless because `node_modules` is usually gitignored. Running `npm ci` or `npm install` on the host later may replace the symlink with a real directory.

## Procedure

1. From the workspace root, run the bundled install script:

```bash
bash scripts/install.sh
```

2. Pass options when needed:

| Option | Description |
| --- | --- |
| `--workspace <path>` | Path to the directory containing `package.json`; auto-detected if omitted. |
| `--playwright` | Also install Playwright Chromium browser and system dependencies for E2E testing. |

3. Let the script copy `package.json`, `package-lock.json`, and `.npmrc` when present to a local ext4 directory.
4. Let the script run `npm ci`, or `npm install` when no lockfile exists, on the local filesystem.
5. Let the script symlink `node_modules` back into the workspace.
6. Let the script verify known native binaries: `esbuild`, `rollup`, `lightningcss`, and `vite` when present.
7. If verification fails, run the script again; first-load native binary failures can be intermittent and non-deterministic.
8. After any `package.json` or `package-lock.json` change, re-run the script.

## Post-install verification

Run the smallest project command that proves the toolchain works:

```bash
npm test
npm run build
npm run dev
```

Use only commands that exist in the project's `package.json` scripts.

## Progressive disclosure and bundled resources

- `scripts/install.sh`: deterministic installer that copies package metadata to local ext4 storage, installs dependencies, creates the `node_modules` symlink, verifies native binaries, and optionally installs Playwright browsers using `sudo` when available.

## Troubleshooting

| Problem | Likely cause | Resolution |
| --- | --- | --- |
| `SIGILL` or `SIGSEGV` when running the dev server | Native binary executed from virtiofs. | Re-run `bash scripts/install.sh`; ensure direct `npm install` was not used in the workspace. |
| `mmap` or `unaligned sysNoHugePageOS` | aarch64 mmap alignment failure from virtiofs. | Install on local ext4 through the script and use the symlinked `node_modules`. |
| `node_modules` not found | Symlink missing or target not created. | Check `ls -la node_modules` and re-run the script. |
| Permission errors | Local deps directory is not writable. | Ensure the container user can write the local install directory. |
| Verification fails intermittently | Native binary first-load crash. | Run the script again before changing project code. |
| Vite cannot serve files through symlink | Vite filesystem allow-list blocks the symlink target. | Add the symlink target's parent, such as `/home/agent/project-deps/`, to `server.fs.allow` in Vite config. |

## Gotchas

- **Do not run `npm ci` or `npm install` directly in the mounted workspace**: native binaries may crash from virtiofs.
- **Do not commit the symlink target**: it is container-local and not part of the repository.
- **Do not assume a broken-looking host symlink is a failure**: validate from inside the container.
- **Do not forget Playwright system dependencies**: use `--playwright` when E2E testing needs Chromium.

## Output template

```markdown
## Sandbox npm install result

**Status:** installed | verified | blocked
**Workspace:** `<path>`
**Install command:** `bash scripts/install.sh [--workspace <path>] [--playwright]`

### Script actions
- Metadata copied: `package.json` | `package-lock.json` | `.npmrc`
- Installer used: `npm ci` | `npm install`
- `node_modules` symlink: present | missing
- Native binary verification: pass | fail | not applicable
- Playwright Chromium: installed | skipped | failed

### Validation
- `npm test`: pass | fail | not run
- `npm run build`: pass | fail | not run
- `npm run dev`: pass | fail | not run

### Notes
<virtiofs, permissions, Vite server.fs.allow, or remaining blocker>
```

## Quality gate

- [ ] The install ran through `bash scripts/install.sh`, not direct workspace `npm ci` or `npm install`.
- [ ] The workspace contains `package.json` and uses the local ext4 install plus `node_modules` symlink.
- [ ] Native binaries `esbuild`, `rollup`, `lightningcss`, and `vite` are verified when present.
- [ ] `--playwright` is used when Chromium E2E support is required.
- [ ] A project-specific validation command from `package.json` was run or explicitly skipped with a reason.
- [ ] Vite projects consider `server.fs.allow` for the symlink target parent.
